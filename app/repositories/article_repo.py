import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from app.models.article import ArticleOrm


logger = logging.getLogger(__name__)


class ArticleRepo:
    @staticmethod
    async def get_all(db: AsyncSession) -> Sequence[ArticleOrm]:
        '''Returns all articles stored in the database from the "main_dictionary" table.'''
        query = select(ArticleOrm)
        logger.debug(f"Query: {query.compile(compile_kwargs={"literal_binds": True})}")
        result = await db.execute(query)
        return result.scalars().all()
    