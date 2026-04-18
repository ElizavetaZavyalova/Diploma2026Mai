import redis
import os
import json

CURRENT = "current"
LAST = "last"
REDIS_HOST = os.environ.get("REDIS_HOST", "10.219.180.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "pass")


class Points:

    def __init__(self, current, last):
        self.current = current
        self.last = last

    def to_dict(self):
        return {
            CURRENT: self.current,
            LAST: self.last
        }

    @staticmethod
    def from_dict(data):
        return Points(
            current=data.get(CURRENT),
            last=data.get(LAST)
        )


class RedisRepository:
    def __init__(self,
                 host=REDIS_HOST,
                 port=REDIS_PORT, password=REDIS_PASSWORD,
                 db=REDIS_DB):
        self.redis = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=True
        )

    def _get(self, key):
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def _get_many(self, keys):
        values = self.redis.mget(keys)
        return {
            key: json.loads(value) if value else None
            for key, value in zip(keys, values)
        }

    def get_point(self, device_id):
        existing = self._get(device_id)
        if existing:
            return Points.from_dict(existing)

    def get_points(self, device_ids:list):
        existing = self._get_many(device_ids)
        if existing:
            return Points.from_dict(existing)
