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
                if quantity >= int(product.quantity):
                    client_redis.hincrby(name=f"stock:{product.product}", key=f"{product.product}",
                                         amount=-int(product.quantity))
                    return {
                        "remainder": quantity - int(product.quantity),
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

    @classmethod
    def show_all_product(cls):
        """Show all products(materials)"""
        with client as client_redis:
            list_products = list()
            for product in client_redis.scan_iter(match="stock:*", count=100):
                list_products.append(client_redis.hgetall(product))
            return list_products
