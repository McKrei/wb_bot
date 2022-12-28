from typing import List, Tuple

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import update, delete
from sqlalchemy.future import select


Base = declarative_base()

class Query(Base):
    __tablename__ = 'query'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    activity = Column(Boolean, nullable=False)
    nm = Column(String, nullable=False)
    query = Column(String, nullable=False)


class QueryDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_query(self, user_id: int, nm: str, query: str):
        new_query = Query(
            user_id=user_id, activity=True, nm=nm, query=query)
        self.db_session.add(new_query)
        await self.db_session.flush()
        return new_query

    async def get_all_active_query(self) -> List[Query]:
            q = await self.db_session.execute(
                select(Query).where(Query.activity == True))
            return q.scalars().all()

    async def get_users_query(self, user) -> Tuple[List[Query]]:
        exec_ = self.db_session.execute
        result = [el.scalars().all() for el in [
            await exec_(select(Query).where(
                Query.user_id == user).where(Query.activity == ac))
                for ac in (True, False)]
                ]
        return result

    async def get_query(self, id) -> List[Query]:
        q = await self.db_session.execute(
            select(Query).where(Query.id == id))
        return q.scalars().all()

    async def update_activity_false(self, id):
        q = update(Query).where(Query.id == id)
        q = q.values(activity=False)
        q.execution_options(synchronize_session="fetch")
        await  self.db_session.execute(q)

    async def deleted_query(self, id):
        q = delete(Query).where(Query.id == id)
        q.execution_options(synchronize_session="fetch")
        await  self.db_session.execute(q)
