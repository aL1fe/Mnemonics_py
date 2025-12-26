from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.repositories.article_repo import ArticleRepo


class ArticleService:
    def __init__(self, article_repo: ArticleRepo):
        self.article_repo = article_repo

    
    async def get_all(self, db: AsyncSession) -> list[Article]:
        atricle_list_orm = await self.article_repo.get_all(db)
        atricle_list = [Article.model_validate(row, from_attributes=True) for row in atricle_list_orm]
        return list(atricle_list)
