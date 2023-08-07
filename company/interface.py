from abc import ABC, abstractmethod


class UICompany(ABC):
    """Interface for Company"""

    @abstractmethod
    def add_company(self, company):
        """Adds company"""
        pass

    @abstractmethod
    def delete_company(self, company):
        """Deletes the company"""
        pass

    def exists_company_name(self, company_name):
        """Checks if a company is added or not"""
        pass

    def product(self, product):
        """Getting product"""
        pass
