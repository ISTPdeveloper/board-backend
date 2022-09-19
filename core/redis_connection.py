import redis


class RedisConnection(object):
    def __init__(self):
        self.conn = redis.StrictRedis(
            host="redis",
            port=6379,
            db=0,
            decode_responses=True,
        )
