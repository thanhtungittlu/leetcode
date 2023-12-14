import json
import time
from abc import abstractmethod
from datetime import datetime, timedelta
from threading import Thread

import redis
import schedule
import unidecode
from dateutil.parser import parse
from mobio.libs.Singleton import Singleton
from mobio.libs.thread_pool import ThreadPool

from mobio.libs.schedule.utils import get_hostname

BEAT_EXTRA_TIME = 5


class SCHEDULER_STATE:
    RUNNING = "running"
    IDLE = "idle"


class BaseScheduler:
    thread_pool = ThreadPool(num_workers=1)
    logger = None
    HEART_BEAT_PREFIX = "heart_beat_"

    # is_running = False

    def __init__(self, name=None, redis_uri=None, beat_time=300):
        self.name = name
        if not redis_uri:
            raise Exception("redis_uri must not be None")
        if not beat_time:
            raise Exception("beat_time must not be None")

        self._redis = redis.from_url(redis_uri)
        if not self.name:
            self.name = self.__class__.__name__
        self.name = unidecode.unidecode(self.name).replace(" ", "")

        self.hostname = get_hostname()

        if beat_time <= 0 or not isinstance(beat_time, int):
            beat_time = 300

        self.beat_time = beat_time
        self.__check_hanging_scheduler()
        self.start_beating()
        self.schedule_job = None

    @abstractmethod
    def get_schedule(self):
        """
        hàm xác định thời điểm chạy của scheduler, bằng cách xử dụng thư viện schedule
        Các ví dụ hướng dẫn cách xác định thời gian chạy
        1. scheduler chỉ thực hiện công việc một lần duy nhất.
            return None
        2. scheduler sẽ thực hiện mỗi 10 phút một lần.
            return schedule.every(10).minutes
        3. scheduler sẽ thực hiện hàng ngày vào lúc 10h 30 phút.
            return schedule.every().day.at("10:30")
        4. scheduler sẽ thực hiện sau mỗi giờ.
            return schedule.every().hour
        5. scheduler sẽ thực hiện vào mỗi thứ 2 hàng tuần.
            return schedule.every().monday
        6. scheduler sẽ thực hiện vào mỗi thứ 5 hàng tuần và vào lúc 13h 15'.
            return schedule.every().wednesday.at("13:15")
        """
        raise NotImplementedError()

    @abstractmethod
    def owner_do(self):
        """
        đây là hàm sẽ thực hiện công việc của scheduler,
        hàm này sẽ được gọi tự động và tự động bắt lỗi ghi log
        """
        pass

    def set_logger(self, logger):
        self.logger = logger

    def __check_hanging_scheduler(self):
        value = self._redis.get(self.name)
        if not value:
            return

        if isinstance(value, bytes):
            value = value.decode("utf-8")

        value = json.loads(value)
        hostname = value['hostname']
        state = value['state']

        if state == SCHEDULER_STATE.RUNNING and hostname == self.hostname:
            self._redis.delete(self.name)

    def __allow_running(self):
        value = self._redis.get(self.name)
        if not value:
            return True, ""

        if isinstance(value, bytes):
            value = value.decode("utf-8")

        value = json.loads(value)
        if value['state'] == SCHEDULER_STATE.RUNNING:
            key = self.HEART_BEAT_PREFIX + value['hostname'] + "_" + self.name
            if self._redis.get(key):
                return False, value['hostname']

        idle_seconds = value.get('idle_seconds') or 0
        last_run = parse(value.get('last_run'))
        next_run = last_run + timedelta(seconds=idle_seconds)
        if next_run > datetime.utcnow():
            return False, value['hostname']
        return True, ""

    def set_state(self, state):
        r = self._redis.get(self.name)
        if r:
            if isinstance(r, bytes):
                r = r.decode("utf-8")
            r = json.loads(r)
        else:
            r = {}

        r['state'] = state
        r['hostname'] = self.hostname

        if state == SCHEDULER_STATE.RUNNING:
            r["last_run"] = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        elif state == SCHEDULER_STATE.IDLE:
            # r["idle_seconds"] = schedule.idle_seconds()
            if 'last_run' not in r:
                r["last_run"] = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
            d1 = self.schedule_job.next_run.timestamp()
            d2 = datetime.now().timestamp()
            r["idle_seconds"] = d1 - d2
        self._redis.set(self.name, json.dumps(r))

    def start_beating(self):
        t = Thread(target=self.__send_heart_beat)
        t.daemon = True
        t.start()

    def __send_heart_beat(self):
        while True:
            key = self.HEART_BEAT_PREFIX + self.hostname + "_" + self.name
            self._redis.set(key, datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"), self.beat_time + BEAT_EXTRA_TIME)
            time.sleep(self.beat_time)

    @thread_pool.thread
    def do(self):
        try:
            is_running, hostname = self.__allow_running()
            if is_running:
                print(datetime.now(), " I'll start my job. ", self.name)
                self.set_state(SCHEDULER_STATE.RUNNING)

                self.owner_do()

                print(datetime.now(), " I'm finished my job. ", self.name)
                self.set_state(SCHEDULER_STATE.IDLE)
            else:
                if hostname == self.hostname:
                    print(datetime.now(), " Please waiting, i'm busy. ", self.name)
                else:
                    print(datetime.now(), " {} is executing.".format(hostname))
        except Exception as e:
            if self.logger:
                self.logger.exception("run job error:%s!" % e)
            else:
                print("run job error:%s!" % e)
            return None
        finally:
            self.set_state(SCHEDULER_STATE.IDLE)


@Singleton
class SchedulerFactory:
    # thread_pool = ThreadPool(num_workers=8)

    def __init__(self):
        self.schedulers = {}
        self.tasks = {}
        self.logger = None

    def set_logger(self, logger):
        self.logger = logger

    def add(self, scheduler: BaseScheduler, scheduler_name=None):
        name = scheduler_name if scheduler_name else scheduler.__class__.__name__
        sq = self.schedulers.get(name, None)
        if sq is None:
            scheduler.set_logger(self.logger)
            the_schedule = scheduler.get_schedule()
            if the_schedule:
                scheduler.schedule_job = the_schedule
                the_schedule.do(scheduler.do)
                self.schedulers[name] = scheduler
            else:
                self.tasks[name] = scheduler
            return scheduler
        return sq

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    # @thread_pool.thread
    # def owner_run_scheduler(self, scheduler: BaseScheduler):
    #     scheduler.do()


if __name__ == '__main__':
    class TestScheduler1(BaseScheduler):
        def __init__(self, name):
            super().__init__(name)

        def get_schedule(self):
            return schedule.every(1).seconds

        def owner_do(self):
            print(datetime.now(), " I'm working. ", self.name)
            time.sleep(3)


    class TestScheduler2(BaseScheduler):
        def __init__(self, name):
            super().__init__(name)

        def get_schedule(self):
            return schedule.every(2).seconds

        def owner_do(self):
            print(datetime.now(), " I'm working. ", self.name)
            time.sleep(3)


    fac = SchedulerFactory()
    fac.add(TestScheduler1('Test1'), 'TestScheduler1')
    fac.add(TestScheduler1('Test2'), 'TestScheduler2')
    fac.run()
