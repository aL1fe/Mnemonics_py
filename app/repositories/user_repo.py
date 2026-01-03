from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from typing import Optional
import logging

from app.models.user import UserOrm


logger = logging.getLogger(__name__)

class UserRepo:
    @staticmethod
    async def create(db: AsyncSession,
        telegram_user_id: int,
        telegram_user_name: Optional[str],
        telegram_first_name: Optional[str],
        telegram_last_name: Optional[str]) -> UserOrm:
        '''
        Creates a new user_orm record with the given Telegram data and returns it.
        '''
        user = UserOrm(
            telegram_user_id=telegram_user_id,
            telegram_user_name=telegram_user_name,
            telegram_first_name=telegram_first_name,
            telegram_last_name=telegram_last_name
        )
        db.add(user)
        await db.flush()  
        await db.refresh(user)
        return user
    

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> UserOrm | None:
        '''
        Retrieves a user_orm by their database ID, also loading the last associated article.
        '''
        query = (select(UserOrm)
                 .where(UserOrm.id == user_id)
                #  .options(selectinload(UserOrm.last_article))
                 .options(joinedload(UserOrm.last_article))
                )
        logger.debug(f"Query: {query.compile(compile_kwargs={"literal_binds": True})}")
        result = await db.execute(query)
        return result.scalar_one_or_none()


    @staticmethod
    async def get_id_by_telegram_id(db: AsyncSession, telegram_user_id: int) -> int | None:
        '''
        Returns the database ID of a user based on their Telegram user ID.
        '''
        query = (select(UserOrm.id)
                 .where(UserOrm.telegram_user_id == telegram_user_id)
                )
        logger.debug(f"Query: {query.compile(compile_kwargs={"literal_binds": True})}")
        result = await db.execute(query)
        user_id = result.scalar_one_or_none()
        return user_id
    

    @staticmethod
    async def update_last_article(db: AsyncSession, user_orm: UserOrm, last_article_id: int) -> None:
        '''
        Updates the last_article_id field for a given user_orm.
        '''
        user_orm.last_article_id = last_article_id
