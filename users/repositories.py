from users.interface import IUserRepository
from redis_connect import client


class RedisRepository(IUserRepository):
    """User interaction with Redis"""

    @classmethod
    def add_user(cls, user):
        """Add user to hash"""
        with client as client_redis:
            client_redis.hset(user.user_id, mapping=user.user_mapping())

    @classmethod
    def delete_user(cls, user_id):
        """Removing a user from hash"""
        with client as client_redis:
            client_redis.hdel(user_id, user_id)
            client_redis.delete(user_id)

    @classmethod
    def generate_user_id(cls):
        """Genreate id for user"""
        with client as client_redis:
            return client_redis.incr("user_id")
