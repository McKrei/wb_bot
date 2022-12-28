'''
Открываем async_session() и отправляем запрос в БД через DAL
'''
from typing import List, Tuple

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from env import DATABASE_URL
from db.models import Query, QueryDAL


engine = create_async_engine(DATABASE_URL, future=True,)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def run_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Query.metadata.drop_all)
        await conn.run_sync(Query.metadata.create_all)
        ...


async def create_query(user_id: int, nm: str, query: str) -> None:
    async with async_session() as session:
        async with session.begin():
            dal = QueryDAL(session)
            return await dal.create_query(user_id, nm, query)


async def get_all_active_query() -> List[Query]:
    async with async_session() as session:
        async with session.begin():
            dal = QueryDAL(session)
            return await dal.get_all_active_query()


async def get_users_query(user: int) -> Tuple[List[Query]]:
    async with async_session() as session:
        async with session.begin():
            dal = QueryDAL(session)
            return await dal.get_users_query(user)


async def update_activity_false(id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            dal = QueryDAL(session)
            return await dal.update_activity_false(id)


async def deleted_query(id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            dal = QueryDAL(session)
            return await dal.deleted_query(id)


async def get_query(id: int) -> Query:
    async with async_session() as session:
        async with session.begin():
            dal = QueryDAL(session)
            return await dal.get_query(id)
