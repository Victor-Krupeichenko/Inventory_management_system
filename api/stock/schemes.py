from pydantic import BaseModel, field_validator, Field


class StockProductScheme(BaseModel):
    """Scheme for add stock"""

    product: str = Field(example="material names")
    quantity: int = Field(example="10 - quantity of materials")

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, quantity):
        """validate field quantity"""

        if not isinstance(quantity, int):
            return {"error": "Quantity must be an integer"}
        if quantity <= 0:
            return {"error": "Quantity must be a positive number"}
        return quantity
