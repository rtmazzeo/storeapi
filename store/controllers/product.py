from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from fastapi.responses import JSONResponse

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


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUsecase = Depends()) -> List[ProductOut]:
    return await usecase.query()


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
