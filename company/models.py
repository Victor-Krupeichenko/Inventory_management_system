from company.repository import CompanyRepositoryRedis
import json


class Company:
    """Model company"""
    __slots__ = ["hash_name", "name", "product", "email"]

    def __init__(self, name, product, email):
        self.hash_name = name
        self.name = name
        self.product = list(product)
        self.email = email

    def company_mapping(self):
        """Return mapping"""
        response = {
            "name": self.name,
            "product": json.dumps(self.product),
            "email": self.email
        }
        return response

    def add_company(self):
        """Add company"""
        CompanyRepositoryRedis.add_company(self)

    @staticmethod
    def delete_company(hash_name):
        """Delete company"""
        CompanyRepositoryRedis.delete_company(hash_name)
