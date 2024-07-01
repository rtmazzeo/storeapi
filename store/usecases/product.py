from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client, get_products_collection
from store.models.product import ProductModel, ProductIn  
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException
from bson import Decimal128


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        product_data = product_model.model_dump()
        product_data["price"] = Decimal128(str(product_model.price))  # Conversão para Decimal128

        try:
            await self.collection.insert_one(product_data)  # Use product_data
        except pymongo.errors.DuplicateKeyError:
            raise InsertError(message="Produto com ID duplicado.")

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
            return [ProductOut(**{**item, "price": item["price"].to_decimal()}) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        update_data = body.model_dump(exclude_none=True)
        if "price" in update_data:
            update_data["price"] = Decimal128(str(update_data["price"]))  # Conversão para Decimal128

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},  # Use update_data
            return_document=pymongo.ReturnDocument.AFTER,
        )
        
        if not result:
            raise NotFoundError(message=f"Product not found with id: {id}")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
