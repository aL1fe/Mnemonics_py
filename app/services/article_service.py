import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.repositories.article_repo import ArticleRepo


logger = logging.getLogger(__name__)


class ArticleService:
    def __init__(self, article_repo: ArticleRepo):
        self.article_repo = article_repo

    
    async def get_all(self, db: AsyncSession) -> list[Article]:
        '''
        Returns all articles stored in the database from the "main_dictionary" table.
        The method retrieves article ORM entities via the repository layer and
        maps them to domain models before returning the result.
        '''
        try:
            atricle_list_orm = await self.article_repo.get_all(db)
            atricle_list = [Article.model_validate(row, from_attributes=True) for row in atricle_list_orm]
            logger.debug(f"Retrieved {len(atricle_list)} articles from the database. Sample: {atricle_list[:3]}")
            return list(atricle_list)
        except Exception as e:
            logger.critical(f"Error while retrieving articles from the 'main_dictionary': {e}")
            return []
