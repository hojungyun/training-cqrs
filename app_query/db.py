from typing import Any, List
from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app_query.models import Product


async def initialize_mongodb_database():
    db_url = "mongodb://localhost:27017/test-db"
    client = AsyncIOMotorClient(db_url)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[
            Product,
        ],
    )


class Database:
    def __init__(self, model):
        self.model = model

    async def create(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs
