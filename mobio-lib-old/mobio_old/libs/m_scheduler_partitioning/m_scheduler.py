import os
from abc import abstractmethod
from datetime import datetime
from threading import Thread
from time import sleep
from kazoo.client import KazooClient
from kazoo.recipe.watchers import DataWatch, ChildrenWatch
from kazoo.exceptions import NodeExistsError
import ast
from mobio.libs.m_scheduler_partitioning import generate_nano_id
from mobio.libs.m_scheduler_partitioning.scheduler_models.scheduler_state_model import (
    SchedulerStateModel,
)


class MobioScheduler:
    rebalancing = False
    lst_partitions = []
    zk_client = None

    def register_worker(self):
        result_register_worker = None
        count_try = 0
        sleep_time = 3
        while not result_register_worker:
            if count_try >= 10:
                sleep_time = 10
            try:
                print(
                    datetime.utcnow(),
                    " waiting for register worker with partitions:",
                    self.lst_partitions,
                )
                result_register_worker = SchedulerStateModel(
                    url_connection=self.url_connection
                ).register_worker(
                    worker_id=self.node_id,
                    partitions=self.lst_partitions,
                    delay_time=self.delays,
                    root_node=self.root_node,
                )
            except Exception as ex:
                print(datetime.utcnow(), " register_worker ERROR: {}".format(ex))
                result_register_worker = None

            if not result_register_worker:
                print(
                    datetime.utcnow(),
                    " register worker ERROR, result: {}".format(result_register_worker),
                )
                sleep(sleep_time)
                count_try += 1
            else:
                print(
                    datetime.utcnow(),
                    " result_register_worker: {}".format(result_register_worker),
                )
                break
        return result_register_worker

    def __send_heart_beat__(self):
        while True:
            result_increase_expiry_time = None
            while not result_increase_expiry_time:
                result_increase_expiry_time = SchedulerStateModel(
                    url_connection=self.url_connection
                ).increase_expiry_time(worker_id=self.node_id, delay_time=self.delays)

                if not result_increase_expiry_time:
                    print(
                        datetime.utcnow(),
                        " send heart beat ERROR, result: {}\n*** Begin re-register worker ...".format(result_increase_expiry_time),
                    )
                    result_register_worker = self.register_worker()
                    print(
                        datetime.utcnow(),
                        " register worker success: {}".format(result_register_worker),
                    )
                else:
                    print(
                        datetime.utcnow(),
                        " result_increase_expiry_time: {}".format(
                            result_increase_expiry_time
                        ),
                    )
            sleep(5)

    def __init__(
        self,
        root_node="test-scheduler",
        node_id=None,
        nop=100,
        delays=1,
        url_connection=None,
        zookeeper_uri=None,
    ):
        if not 10 <= nop <= 1000:
            raise Exception("nop {} not in range 10, 1000".format(nop))

        if delays > 3600:
            raise Exception("delays maximum is 3600 seconds")
        elif delays < 1:
            raise Exception("delays minimum is 1 second")

        if zookeeper_uri:
            self.zookeeper_uri = zookeeper_uri
        else:
            self.zookeeper_uri = os.getenv("ZOOKEEPER_CLUSTER")

        self.root_path = "/mobio-scheduler/{}".format(root_node)
        self.root_node = root_node
        self.nop = nop
        self.delays = delays
        self.url_connection = url_connection
        if not node_id:
            node_id = generate_nano_id(short=True)
        self.node_id = node_id
        self.my_node_path = "{}/{}".format(self.root_path, node_id)

        self.zk_client = KazooClient(hosts=self.zookeeper_uri)
        self.zk_client.start()
        self.zk_client.ensure_path(self.root_path)
        print("ensure root path: {}".format(self.root_path))
        sleep(1)
        self.subscribe_to_node()
        ChildrenWatch(
            client=self.zk_client,
            path=self.root_path,
            func=self.watch_children,
            send_event=True,
        )
        DataWatch(
            client=self.zk_client,
            path=self.root_path,
            func=self.watch_data_root,
            send_event=True,
        )
        DataWatch(
            client=self.zk_client,
            path=self.my_node_path,
            func=self.watch_data_children,
            send_event=True,
        )
        if self.url_connection:
            t = Thread(target=self.__send_heart_beat__)
            t.daemon = True
            t.start()

        try:
            while True:
                if self.check_is_subscribed():
                    if self.url_connection:
                        result_busy = None
                        counter_busy = 0
                        sleep_time_busy = 1
                        while not result_busy:
                            if counter_busy >= 3:
                                sleep_time_busy = 10
                            result_busy = SchedulerStateModel(
                                url_connection=self.url_connection
                            ).set_busy(worker_id=self.node_id)
                            if result_busy:
                                print(
                                    datetime.utcnow(),
                                    " result busy_worker: {}".format(result_busy),
                                )
                            else:
                                print(
                                    datetime.utcnow(),
                                    " Set Busy ERROR. Begin sleep {} second{} to ensure busy".format(
                                        sleep_time_busy, "" if sleep_time_busy == 1 else "s"
                                    ),
                                )
                                sleep(sleep_time_busy)
                                counter_busy += 1
                    self.process()
                    print(
                        datetime.utcnow(),
                        " {} still alive after: {} seconds".format(self.node_id, self.delays),
                    )
                    if self.url_connection:
                        result_release = None
                        counter_release = 0
                        sleep_time_release = 1
                        while not result_release:
                            if counter_release >= 3:
                                sleep_time_release = 10
                            result_release = SchedulerStateModel(
                                url_connection=self.url_connection
                            ).release_worker(worker_id=self.node_id)
                            if result_release:
                                print(
                                    datetime.utcnow(),
                                    "result release_worker: {}".format(result_release),
                                )
                            else:
                                print(
                                    datetime.utcnow(),
                                    " Release Worker ERROR. Begin sleep {} second{} to ensure busy".format(
                                        sleep_time_release, "" if sleep_time_release == 1 else "s"
                                    ),
                                )
                                sleep(sleep_time_release)
                                counter_release += 1
                else:
                    print(
                        datetime.utcnow(),
                        " worker: {} is not subscribed\n*** Begin re-subscribe worker ...".format(self.node_id),
                    )
                    self.subscribe_to_node()
                sleep(self.delays)
        except RuntimeError as e:
            print(
                datetime.utcnow(),
                " something unexpected happened: {}: {}".format(self.my_node_path, e),
            )
        finally:
            print(datetime.utcnow(), " consumer is stopped")
            self.zk_client.stop()
            self.zk_client.close()

    def subscribe_to_node(self):
        try:
            subscribed_value = self.zk_client.create(self.my_node_path, ephemeral=True)
            print(datetime.utcnow(), " subscribe_to_node: {}".format(subscribed_value))
        except NodeExistsError as nee:
            print(datetime.utcnow(), " worker already subscribed")

        sleep(1)

    @abstractmethod
    def process(self):
        print(datetime.utcnow(), " in process")
        if self.rebalancing:
            print(
                datetime.utcnow(),
                " in process: rebalancing: {}".format(self.rebalancing),
            )
            self.rebalancing = False
            print(
                datetime.utcnow(),
                " in process: rebalancing: {}".format(self.rebalancing),
            )
        """
        sample code:
        
        limit = 1000
        has_data = True
        sequence_id = 0
        lst_ids = []
        while has_data:
            lst_job = self.get_jobs(
                sequence_id=sequence_id, limit=limit
            )
            if len(lst_job) < limit:
                has_data = False
            for current_job in lst_job:
                if self.rebalancing:
                    if lst_ids:
                        self.save_to_sent_batch(lst_ids=lst_ids)
                        lst_ids = []
                        ConfluentProducerManager().flush_to_topic()
                    has_data = False
                    sys_conf.logger.warning(
                        "rebalancing in row: {}".format(current_msg.get("_id"))
                    )
                    self.rebalancing = False
                    break
    
                try:
                    sequence_id = current_job.get("sequence_id")
                    key = current_job.get("profile_id")
                    ConfluentProducerManager().send_message_to_topic_with_key_without_flush(
                        topic=KafkaTopic.FACTORY_F1_JB_ABANDONED_CART,
                        data=json.dumps(
                            json.loads(JSONEncoder().encode(current_job))
                        ).encode("utf-8"),
                        key=str(key),
                    )
    
                    lst_ids.append(_id)
                    if len(lst_ids) % 20 == 0:
                        self.save_to_sent_batch(lst_ids=lst_ids)
                        lst_ids = []
                        ConfluentProducerManager().flush_to_topic()
                except Exception as er:
                    err_msg = "do_process:: cannot sent data ERROR: {}".format(er)
                    sys_conf.logger.error(err_msg)
            if lst_ids:
                self.save_to_sent_batch(lst_ids=lst_ids)
                lst_ids = []
                ConfluentProducerManager().flush_to_topic()
        """

    # function theo dõi sự thay đổi của các workers.
    # Nếu có worker join hoặc leave parent thì sẽ assign lại partitions cho các workers
    def watch_children(self, lst_children, event=None):
        print(
            datetime.utcnow(),
            " Children are now: {}, event: {}".format(
                lst_children, event if event else ""
            ),
        )
        # self.rebalance_current_node()
        num_child = len(lst_children)
        lst = [x for x in range(self.nop)]
        tmp_lst_partitions = self.split(lst, num_child)
        for i in range(num_child):
            value = bytes(str(tmp_lst_partitions[i]), "utf-8")
            self.zk_client.set(
                "{}/{}".format(self.root_path, lst_children[i]), value=value
            )
        print(datetime.utcnow(), " set data done")

    # function notify số lượng partitions mà worker này sẽ xử lý
    def watch_data_root(self, data, stat, event=None):
        print(
            datetime.utcnow(),
            " Version: %s, data: %s, event: %s"
            % (stat.version, data.decode("utf-8"), event if event else ""),
        )

    def check_is_subscribed(self):
        lst_children = self.zk_client.get_children(path=self.root_path)
        return True if self.node_id in lst_children else False

    # function notify cho worker là cần rebalance lại partitions
    def watch_data_children(self, data, stat, event=None):
        print(
            datetime.utcnow(),
            " watch_data_children:: Version: %s, data: %s, event: %s"
            % (stat.version, data.decode("utf-8"), event),
        )
        d = data.decode("utf-8")
        self.rebalancing = True
        self.lst_partitions = []
        if d:
            try:
                self.lst_partitions = ast.literal_eval(d)
            except Exception as ex:
                print(datetime.utcnow(), " ERROR:: {} when eval data: {}".format(ex, d))
        if not self.lst_partitions:
            raise Exception(
                "current partitions is null with data: {}, please check......".format(d)
            )
        print(datetime.utcnow(), " current partition: {}".format(self.lst_partitions))
        if self.url_connection:
            result = None
            while not result:
                if self.url_connection:
                    result = SchedulerStateModel(
                        url_connection=self.url_connection
                    ).rebalance_partitions(
                        worker_id=self.node_id, partitions=self.lst_partitions
                    )
                    print(datetime.utcnow(), " result rebalance: {}".format(result))
                if not result:
                    result_register_worker = self.register_worker()
                    print(
                        datetime.utcnow(),
                        " register worker success: {}".format(result_register_worker),
                    )

    def split(self, a, n):
        k, m = divmod(len(a), n)
        return list(
            a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)
        )


if __name__ == "__main__":
    MobioScheduler()
