from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Sequence

from app.models.user import User
from app.models.user_article import UserArticle, UserArticleOrm


class UserArticleRepo:
    @staticmethod
    async def bulk_create(db: AsyncSession, user: User, user_article_list: list[UserArticle]) -> None:
        '''
        Creates multiple UserArticle records for a given user in a single database operation.   
        '''
        user_articles_orm = [
            UserArticleOrm(
                user_id=user.id, 
                article_id=user_article.article.id,
                weight=user_article.weight
            )
            for user_article in user_article_list
        ]
        db.add_all(user_articles_orm)
        await db.commit()


    @staticmethod
    async def get_vocabulary(db: AsyncSession, user_id: int) -> Sequence[UserArticleOrm]:
        '''
        Returns the full vocabulary (articles) associated with the given user.
        '''
        query = (select(UserArticleOrm)
                 .options(joinedload(UserArticleOrm.article))  # Eagerly loading strategy
                 .where(UserArticleOrm.user_id == user_id)
        )
        result = await db.execute(query)       
        return result.scalars().all()
    
    
    @staticmethod
    async def get(db: AsyncSession, user_id: int, artilce_id: int) -> UserArticleOrm | None:
        '''
        Retrieves a specific UserArticle record for the given user and article IDs.  
        '''
        query = (select(UserArticleOrm)
                 .where(UserArticleOrm.user_id == user_id,
                        UserArticleOrm.article_id == artilce_id)
                )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    

    @staticmethod
    async def update_weight(db: AsyncSession, user_artilce: UserArticleOrm, weight: int) -> None:
        '''
        Updates the weight of a user's article by applying the given delta value.
        '''
        user_artilce.weight = weight
        await db.commit()
    