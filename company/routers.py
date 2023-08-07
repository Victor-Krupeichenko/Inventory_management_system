from fastapi import APIRouter, status
from company.models import Company
from company.schemes import CompanyCreateScheme
from company.repository import CompanyRepositoryRedis
from utils import error_checking

company_router = APIRouter(prefix="/company", tags=["company"])


@company_router.post("/add_company")
async def add_company(company: CompanyCreateScheme):
    """Adds a company"""
    data = dict(company)
    errors = await error_checking(data, "error")
    if errors:
        return errors
    try:
        new_company = Company(name=data.get("name"), product=data.get("product"), email=data.get("email"))
        new_company.add_company()
        response = {
            "status": status.HTTP_201_CREATED,
            "add company": data.get("name")
        }
        return response
    except Exception as ex:
        return {"error": f"{ex}", "status": status.HTTP_400_BAD_REQUEST}


@company_router.get("/company_specified/{product}")
def company_specified_product(product):
    """Displays all companies that have the specified product"""
    try:
        return CompanyRepositoryRedis.product(product)
    except Exception as ex:
        return {"error": f"{ex}", "status": status.HTTP_400_BAD_REQUEST}
