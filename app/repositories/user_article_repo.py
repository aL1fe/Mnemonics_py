from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from typing import Sequence

from app.models.user import User
from app.models.user_article import UserArticle, UserArticleOrm


class UserArticleRepo:
    @staticmethod
    async def bulk_create(db: AsyncSession, user: User, user_article_list: list[UserArticle]) -> None:
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
        The method retrieves all UserArticle records for the specified user ID,
        eagerly loading the related Article entities to avoid additional database queries.
        '''
        query = (select(UserArticleOrm)
                 .options(joinedload(UserArticleOrm.article))  # Eagerly loading strategy
                #  .options(selectinload(UserArticleOrm.article))  # Lazy loading strategy          
                 .where(UserArticleOrm.user_id == user_id)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))  # Show the generated SQL query
        result = await db.execute(query)       
        return result.scalars().all()
    
    
    @staticmethod
    async def get(db: AsyncSession, user_artilce_id: int) -> UserArticleOrm | None:
        user_artilce = await db.get(UserArticleOrm, user_artilce_id)
        return user_artilce
    

    @staticmethod
    async def update_weight(db: AsyncSession, user_artilce: UserArticleOrm, weight: int) -> None:
        '''
        Updates the weight of a user's article by applying the given delta value.
        The method finds the UserArticle record by its ID and increments (or decrements)
        its weight, then commits the changes to the database.
        '''
        user_artilce.weight = weight
        await db.commit()
    