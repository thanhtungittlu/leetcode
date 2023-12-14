from datetime import datetime, timedelta

from mobio.libs.m_scheduler_partitioning import SingletonArgs
from mobio.libs.m_scheduler_partitioning.scheduler_models.base_model import BaseModel


class SchedulerState:
    BUSY = "busy"
    FREE = "free"


class SchedulerStateModel(BaseModel, metaclass=SingletonArgs):
    ID = "_id"
    STATE = "state"
    EXPIRY_TIME = "expiry_time"
    PARTITIONS = "partitions"
    ROOT_NODE = "root_node"

    EXPIRY_EXTRA_TIME = 15

    def __init__(self, url_connection):
        super(SchedulerStateModel, self).__init__(url_connection)
        self.collection = "scheduler_state"

    def register_worker(self, worker_id, partitions, root_node, delay_time):
        raw_result = self.get_db().update(
            {
                self.ID: worker_id,
            },
            {
                "$set": {
                    self.ID: worker_id,
                    self.STATE: SchedulerState.FREE,
                    self.PARTITIONS: partitions,
                    self.ROOT_NODE: root_node,
                    self.EXPIRY_TIME: datetime.utcnow()
                    + timedelta(seconds=delay_time + self.EXPIRY_EXTRA_TIME),
                    self.UPDATED_TIME: datetime.utcnow(),
                },
                "$setOnInsert": {self.CREATED_TIME: datetime.utcnow()},
            },
            upsert=True,
        )
        return (
            worker_id
            if (raw_result.get("upserted") or raw_result.get("updatedExisting"))
            else None
        )

    def release_worker(self, worker_id):
        return (
            self.get_db()
            .update_one(
                {self.ID: worker_id},
                {
                    "$set": {
                        self.STATE: SchedulerState.FREE,
                        self.UPDATED_TIME: datetime.utcnow(),
                    }
                },
            )
            .matched_count
        )

    def increase_expiry_time(self, worker_id, delay_time):
        return (
            self.get_db()
            .update_one(
                {self.ID: worker_id},
                {
                    "$set": {
                        # self.STATE: SchedulerState.FREE,
                        self.EXPIRY_TIME: datetime.utcnow()
                        + timedelta(seconds=delay_time + self.EXPIRY_EXTRA_TIME),
                        self.UPDATED_TIME: datetime.utcnow(),
                    }
                },
            )
            .matched_count
        )

    def rebalance_partitions(self, worker_id, partitions):
        return (
            self.get_db()
            .update_one(
                {self.ID: worker_id},
                {
                    "$set": {
                        self.PARTITIONS: partitions,
                        self.UPDATED_TIME: datetime.utcnow(),
                    }
                },
            )
            .matched_count
        )

    def set_state(self, worker_id, state):
        return (
            self.get_db()
            .update_one(
                {self.ID: worker_id},
                {"$set": {self.STATE: state, self.UPDATED_TIME: datetime.utcnow()}},
            )
            .matched_count
        )

    def set_busy(self, worker_id):
        return (
            self.get_db()
            .update_one(
                {self.ID: worker_id},
                {
                    "$set": {
                        self.STATE: SchedulerState.BUSY,
                        self.UPDATED_TIME: datetime.utcnow(),
                    }
                },
            )
            .matched_count
        )

    def get_free_worker(self, root_node):
        result = self.get_db().find(
            {self.ROOT_NODE: root_node, self.STATE: SchedulerState.FREE}
        )
        return list(result)
