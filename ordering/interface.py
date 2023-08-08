from abc import ABC, abstractmethod


class UIOrder(ABC):
    """Interface for Order"""

    @abstractmethod
    def balance_for_order(self, remainder, product):
        """Balance for order"""
        pass
