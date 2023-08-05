import redis
from settings_env import redis_host, redis_port, redis_db

client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
