import redis
import config.settings.env as ENV


class RedisConnection(object):
    def __init__(self):
        self.conn = redis.StrictRedis(
            host=ENV.REDIS_HOST, port=ENV.REDIS_PORT, db=0, decode_responses=True
        )
