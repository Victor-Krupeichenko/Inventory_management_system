from api.stock.interface import UIStock
from connect_db import client


class StockRepositoryRedis(UIStock):
    """Interface for interacting with Redis"""

    @classmethod
    def add_product(cls, product):
        """Adds a product"""

        with client as client_redis:
            if client_redis.exists(f"stock:{product.product}"):
                client_redis.hincrby(name=f"stock:{product.product}", key=f"{product.product}", amount=product.quantity)
            else:
                client_redis.hset(name=f"stock:{product.product}", key=f"{product.product}", value=product.quantity)

    @classmethod
    def consumption(cls, product):
        """Stock consumption"""
        with client as client_redis:
            if client_redis.exists(f"stock:{product.product}"):
                quantity = int(client_redis.hget(name=f"stock:{product.product}", key=f"{product.product}"))
                if quantity >= product.quantity:
                    client_redis.hincrby(name=f"stock:{product.product}", key=f"{product.product}",
                                         amount=-product.quantity)
                    return {
                        "remainder": quantity - product.quantity,
                        "spend": product.quantity
                    }
                else:
                    client_redis.hincrby(name=f"stock:{product.product}", key=f"{product.product}", amount=-quantity)
                    return {
                        "remainder": 0,
                        "spend": quantity
                    }
            else:
                return False
