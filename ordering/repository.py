from ordering.interface import UIOrder
from connect_db import client

MIN_QUANTITY = 10


class OrderRepositoryRedis(UIOrder):
    """Interface for interacting with Redis"""

    @classmethod
    async def balance_for_order(cls, remainder, product):
        """Balance for order"""
        with client as client_redis:
            for email in client_redis.hvals(name=f"product:{product}"):
                client_redis.rpush("application", email)
            await cls.send_application()

    @staticmethod
    async def send_application():
        """Sends an application"""
        with client as client_redis:
            if client_redis.exists("application"):
                while True:
                    email = client_redis.blpop(keys="application")
                    print(f"sent to {email[1]}")
                    if not client_redis.exists("application"):
                        break
            else:
                return {"message": "not found"}
