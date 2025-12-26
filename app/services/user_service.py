from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.user import User
from app.models.user_article import UserArticle
from app.repositories.user_repo import UserRepo


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    
    async def create(
        self,
        db: AsyncSession,
        telegram_user_id: int,
        telegram_user_name: Optional[str],
        telegram_first_name: Optional[str],
        telegram_last_name: Optional[str]
    ) -> User:
        user_orm = await self.user_repo.create(
            db, 
            telegram_user_id, 
            telegram_user_name, 
            telegram_first_name, 
            telegram_last_name,
            )
        user = User(
            id=user_orm.id,
            telegram_user_id=user_orm.telegram_user_id,
            telegram_user_name=user_orm.telegram_user_name,
            telegram_first_name=user_orm.telegram_first_name,
            telegram_last_name=user_orm.telegram_last_name,
            last_article=None,
            user_article_list=[]
        )
        return user


    async def get_id_by_telegram_id(self, db: AsyncSession, telegram_user_id: int) -> int | None:
        return await self.user_repo.get_id_by_telegram_id(db, telegram_user_id)
    