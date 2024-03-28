from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCursor
from pymongo.results import InsertManyResult, UpdateResult, DeleteResult
from bson import ObjectId
from typing import Optional, Any, TypedDict, NotRequired, Sequence, Mapping

__all__ = (
    'MongoDB',
)


class Document(TypedDict, total=False):
    _id: ObjectId


class CursorSort(TypedDict):
    key_or_list:  str | Sequence[str | tuple[str, int | str | Mapping[str, Any]]] | Mapping[str, Any]
    direction: NotRequired[int | str]


class MongoDB(AsyncIOMotorClient):
    def __init__(self, uri: str, db_name: str, collection_name: str) -> None:
        super().__init__(uri)
        self.collection = self[db_name][collection_name]

    async def len(self, option: Optional[Any] = None) -> int:
        return await self.collection.count_documents(option if option else {})

    async def updateOne(self, option: str | Document | Any, update: str | Document | Any) -> UpdateResult:
        return await self.collection.update_one(option, update)

    async def updateMany(self, option: str | Document | Any, update: str | Document | Any) -> UpdateResult:
        return await self.collection.update_many(option, update)

    async def insert(self, data: list[dict] | dict) -> InsertManyResult:
        return await self.collection.insert_many(data if isinstance(data, list) else [data])

    async def deleteOne(self, option: Optional[Document | Any]) -> DeleteResult:
        return await self.collection.delete_one(option)

    async def deleteMany(self, option: Optional[Document | Any]) -> DeleteResult:
        return await self.collection.delete_many(option)

    async def find(self, *, limit: Optional[int] = None, option: Optional[Document | Any] = None, sort: Optional[CursorSort] = None, skip: int = 0) -> AsyncIOMotorCursor | Document:
        if limit == 1:
            return await self.collection.find_one(option)
        else:
            return getattr(cursor, 'sort')(**sort) if (sort, cursor := self.collection.find(option).skip(skip))[0] else getattr(cursor, 'limit')(limit) if limit else cursor
