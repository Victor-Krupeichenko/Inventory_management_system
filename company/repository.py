from company.interface import UICompany
from connect_db import client


class CompanyRepositoryRedis(UICompany):
    """Interface for interacting with Redis"""

    @classmethod
    def add_company(cls, company):
        """Adds company"""

        with client as client_redis:
            # Добавляем компанию в хранилище
            client_redis.hset(name=f"name_{company.name}", mapping=company.company_mapping())
            for product in company.product:
                client_redis.sadd(f"{product}", f"{company.email}")  # Добавляем email в множество для продукта
                client_redis.hset(name=f"product:{product}", key=f"{company.name}", value=company.email)

    @classmethod
    def delete_company(cls, company):
        """Deletes the company"""

        with client as client_redis:
            client_redis.hdel(company, company)
            client_redis.delete(company)

    @classmethod
    def exists_company_name(cls, company_name):
        """Checks if a company is added or not"""

        with client as client_redis:
            if client_redis.exists(f"name_{company_name}"):
                return {"error": "This company has already been added"}
            return company_name

    @classmethod
    def product(cls, product):
        """Getting product"""

        with client as client_redis:
            response = {
                "company": client_redis.hgetall(name=f"product:{product}")
            }
            return response
