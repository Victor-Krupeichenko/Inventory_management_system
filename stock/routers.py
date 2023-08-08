from fastapi import APIRouter
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
        "product": data.get("product"),
        "quantity": data.get("quantity")
    }
