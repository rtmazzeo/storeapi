from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from fastapi.responses import JSONResponse
from fastapi import Query

from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase, NotFoundError

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.create(body=body)
    except InsertError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(id: UUID = Path(alias="id"), usecase: ProductUsecase = Depends()) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get("/", response_model=List[ProductOut])  # Assumindo que você tem um schema ProductOut
async def get_products(
    min_price: float = Query(None, ge=0),
    max_price: float = Query(None, ge=0),
    product_usecase: ProductUsecase = Depends(),
):
    if min_price is not None:
        min_price = Decimal128(str(min_price))
    if max_price is not None:
        max_price = Decimal128(str(max_price))

    return await product_usecase.get_products_by_price_range(min_price, max_price) 


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
  id: UUID = Path(alias="id"),
  body: ProductUpdate = Body(...),
  usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
  try:
    return await usecase.update(id=id, body=body)
  except NotFoundError as e:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(e)}  
    )


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
  id: UUID = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
  try:
    await usecase.delete(id=id)
  except NotFoundError as e:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(e)}  
    )
