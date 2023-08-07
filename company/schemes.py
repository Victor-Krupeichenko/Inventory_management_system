from pydantic import BaseModel, field_validator
from email_validator import validate_email, EmailNotValidError
from company.repository import CompanyRepositoryRedis


class CompanyCreateScheme(BaseModel):
    """Scheme for adds company"""

    name: str
    product: list
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, email):
        """Validate field email"""
        try:
            validate_email(email)
        except EmailNotValidError:
            return {"error": "Email is not valid"}
        return email

    @field_validator("name")
    @classmethod
    def validate_name(cls, company_name):
        """Validate field name"""
        company = CompanyRepositoryRedis.exists_company_name(company_name)
        if isinstance(company, dict):
            return company
        return company_name

    @field_validator("product")
    @classmethod
    def validate_product(cls, product):
        """Validate field product"""
        if not product:
            return {"error": "there must be at least one entry"}
        return product
