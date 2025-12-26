from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from typing import Optional

from app.models.user import UserOrm
from app.models.user_article import UserArticle


class UserRepo:
    @staticmethod
    async def create(
        db: AsyncSession,
        telegram_user_id: int,
        telegram_user_name: Optional[str],
        telegram_first_name: Optional[str],
        telegram_last_name: Optional[str]
    ) -> UserOrm:
        user = UserOrm(
            telegram_user_id=telegram_user_id,
            telegram_user_name=telegram_user_name,
            telegram_first_name=telegram_first_name,
            telegram_last_name=telegram_last_name
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    

    @staticmethod
    async def get_by_telegram_id(db: AsyncSession, telegram_user_id: int) -> UserOrm | None:
        query = (select(UserOrm)
                 .where(UserOrm.telegram_user_id == telegram_user_id)
                )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await db.execute(query)
        return result.scalar_one_or_none()


    @staticmethod
    async def get_id_by_telegram_id(db: AsyncSession, telegram_user_id: int) -> int | None:
        query = (select(UserOrm.id)
                 .where(UserOrm.telegram_user_id == telegram_user_id)
                )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await db.execute(query)
        return result.scalar_one_or_none()    
    

    @staticmethod
    async def delete(db: AsyncSession, user: UserOrm):
        await db.delete(user)
        await db.commit()
