from abc import ABC, abstractmethod


class UIStock(ABC):
    """Interface for Stock"""

    @abstractmethod
    def add_product(self, product):
        """Adds a product"""
        pass

    @abstractmethod
    def consumption(self, product):
        """Stock consumption"""
        pass
