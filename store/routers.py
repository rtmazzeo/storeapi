from fastapi import APIRouter
from store.controllers.product import router as product
from bson import Decimal128

api_router = APIRouter()
api_router.include_router(product, prefix="/products")
