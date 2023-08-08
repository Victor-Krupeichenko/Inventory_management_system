from fastapi import APIRouter, status
from stock.schemes import StockProductScheme
from stock.models import Stock
from utils import error_checking

stock_router = APIRouter(prefix="/stock", tags=["stock"])


@stock_router.post("/add_stock")
async def create_stock(product: StockProductScheme):
    """Adds product"""

    data = dict(product)
    errors = await error_checking(data, "error")
    if errors:
        return errors

    new_product = Stock(**data)
    new_product.add_product()

    return {
        "status": status.HTTP_201_CREATED,
        "product": data.get("product"),
        "quantity": data.get("quantity")
    }


@stock_router.post("/stock_consumption")
async def stock_consumption(product: StockProductScheme):
    """Stock consumption"""
    data = dict(product)
    errors = await error_checking(data, "error")
    if errors:
        return errors
    consumption_stock = Stock(**data)
    remainder = consumption_stock.consumption()
    if not remainder:
        return {
            "error": "no such material",
            "status": status.HTTP_400_BAD_REQUEST
        }
    return {
        "remainder": remainder,
        "status": status.HTTP_202_ACCEPTED
    }
