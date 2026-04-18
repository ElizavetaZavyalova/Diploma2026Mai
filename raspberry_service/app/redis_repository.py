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

    def _set(self, key, value: dict):
        self.redis.set(key, json.dumps(value))

    def _get(self, key):
        value = self.redis.get(key)
        return json.loads(value) if value else None

    def set_point(self, device_id, point):
        existing = self._get(device_id)

        last_point = None
        if existing:
            last_point = existing.get(CURRENT)

        new_point = Points(current=point, last=last_point)

        self._set(device_id, new_point.to_dict())
