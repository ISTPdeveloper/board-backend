import os
import redis


class RedisConnection(object):
    def __init__(self):
        self.conn = redis.StrictRedis(
            host=os.getenv("REDIS_PORT"),
            port=os.getenv("REDIS_PORT"),
            db=0,
            decode_responses=True,
        )
