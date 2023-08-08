from stock.repository import StockRepositoryRedis


class Stock:
    """To represent inventory in a warehouse"""

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def add_product(self):
        """Adds a product"""
        StockRepositoryRedis.add_product(self)
