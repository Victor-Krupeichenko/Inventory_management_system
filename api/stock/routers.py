from fastapi import APIRouter, status
from api.stock.schemes import StockProductScheme
from api.stock.models import Stock
from api.utils import error_checking
from api.ordering.repository import OrderRepositoryRedis, MIN_QUANTITY as min_quantity

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
    answer = consumption_stock.consumption()
    if not answer:
        return {
            "error": "no such material",
            "status": status.HTTP_400_BAD_REQUEST
        }

    if answer.get("remainder") <= min_quantity:
        await OrderRepositoryRedis.balance_for_order(answer.get("remainder"), data.get("product"))
    return {
        "remainder": answer,
        "status": status.HTTP_202_ACCEPTED
    }
