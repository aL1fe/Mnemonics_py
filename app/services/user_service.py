from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.article import Article
from app.models.user import User, UserOrm
from app.models.user_article import UserArticle
from app.repositories.user_repo import UserRepo


def map_user_orm_to_user(user_orm: UserOrm) -> User:
    last_article = None
    if user_orm.last_article:
        last_article = Article(
            id=user_orm.last_article.id,
            eng_word=user_orm.last_article.eng_word,
            ukr_word=user_orm.last_article.ukr_word,
        )
    return User(
        id=user_orm.id,
        telegram_user_id=user_orm.telegram_user_id,
        telegram_user_name=user_orm.telegram_user_name,
        telegram_first_name=user_orm.telegram_first_name,
        telegram_last_name=user_orm.telegram_last_name,
        is_sync=user_orm.is_sync,
        last_article=last_article,
        user_article_list=[]
    )

class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    
    async def create(self,
        db: AsyncSession,
        telegram_user_id: int,
        telegram_user_name: Optional[str],
        telegram_first_name: Optional[str],
        telegram_last_name: Optional[str]) -> User:

        user_orm = await self.user_repo.create(db, 
            telegram_user_id, 
            telegram_user_name, 
            telegram_first_name, 
            telegram_last_name)
        return map_user_orm_to_user(user_orm)
    

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        user_orm = await self.user_repo.get_by_id(db, user_id)
        return map_user_orm_to_user(user_orm) if user_orm else None
    

    async def get_id_by_telegram_id(self, db: AsyncSession, telegram_user_id: int) -> int | None:
        return await self.user_repo.get_id_by_telegram_id(db, telegram_user_id)

    
    async def update_last_article(self, db: AsyncSession, user_id: int, last_article_id: int) -> None:
        user_orm = await self.user_repo.get_by_id(db, user_id)
        if user_orm is not None:
            await self.user_repo.update_last_article(db, user_orm, last_article_id)
        

    # async def get_last_article_id_by_user_id(self, db: AsyncSession, telegram_user_id: int) -> int | None:
    #     return await self.user_repo.get_last_article_id_by_user_id(db, telegram_user_id)    



