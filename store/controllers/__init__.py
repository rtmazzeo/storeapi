from fastapi import HTTPException, status

class InsertionError(Exception):
    def __init__(self, message: str):
        self.message = message


# Exemplo de controller (adapte para o seu caso específico)
from fastapi import APIRouter
from . import schemas, usecases  # Importe seus schemas e usecases

router = APIRouter()

@router.post("/products/", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate):
    try:
        return await usecases.create_product(product)
    except InsertionError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
