from users.interface import IUserRepository
from redis_connect import client


class RedisRepository(IUserRepository):
    """User interaction with Redis"""

    @classmethod
    def add_user(cls, user):
        """Add user to hash"""
        with client as client_redis:
            client_redis.hset(user.user_hash, mapping=user.user_mapping())

    @classmethod
    def delete_user(cls, user_hash):
        """Removing a user from hash"""
        with client as client_redis:
            client_redis.hdel(user_hash, user_hash)
            client_redis.delete(user_hash)
