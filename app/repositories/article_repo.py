from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from typing import Sequence

from app.models.article import ArticleOrm


class ArticleRepo:
    @staticmethod
    async def get_all(db: AsyncSession) -> Sequence[ArticleOrm]:
        query = select(ArticleOrm)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await db.execute(query)       
        return result.scalars().all()