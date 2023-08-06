from users.interface import IUserRepository, IUserAuth
from connect_db import client


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

    @classmethod
    def get_user(cls, username):
        """Getting a user from the database"""
        with client as client_redis:
            return client_redis.hgetall(name=username)


class RedisAuthUser(IUserAuth):
    """Checking users in redis"""

    @classmethod
    def exists_user(cls, username, flag=None):
        """There is a user in the database"""
        if flag:
            with client as client_redis:
                if client_redis.exists(username):
                    return {"error": f"user with name: {username} already exists"}
        else:
            with client as client_redis:
                if not client_redis.exists(username):
                    return {"error": f"username: {username} does not exist"}
                return username

    @classmethod
    def get_password(cls, values):
        """Getting a password"""
        with client as client_redis:
            hash_pass = client_redis.hget(name=values.data.get("username"), key="password")
            return hash_pass
