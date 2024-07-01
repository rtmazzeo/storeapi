from store.models.base import CreateBaseModel
from store.schemas.product import ProductIn
from pydantic import Field

class ProductModel(ProductIn, CreateBaseModel):
    price: float = Field(..., gt=0, description="Preço do produto")
