from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

from app.models.article import Article
from app.models.user import User, UserOrm
from app.repositories.user_repo import UserRepo


logger = logging.getLogger(__name__)


def map_user_orm_to_user(user_orm: UserOrm) -> User:
    '''
    Converts a UserOrm object to a domain User object, including mapping the last article if it exists.
    '''
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
        telegram_last_name: Optional[str]) -> User | None:
        '''
        Creates a new user in the database and returns it as a domain User object.
        '''
        try:
            user_orm = await self.user_repo.create(db, 
                telegram_user_id, 
                telegram_user_name, 
                telegram_first_name, 
                telegram_last_name)            
            logger.info(f"User created successfully: id={user_orm.id}, telegram_user_id={telegram_user_id}")
            return map_user_orm_to_user(user_orm)
        except Exception as e:
            logger.critical(f"Failed to create user with telegram_user_id={telegram_user_id}: {e}")
            return None
            

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        '''
        Retrieves a user by ID and returns it as a domain User, or None if not found.
        '''
        logger.debug(f"Attempting to get user with id={user_id}")
        try:
            user_orm = await self.user_repo.get_by_id(db, user_id)
            if user_orm:
                logger.debug(f"User found: id={user_id}, telegram_user_id={user_orm.telegram_user_id}")
                return map_user_orm_to_user(user_orm)
  
            logger.warning(f"User with id={user_id} not found")
            return None
        except Exception as e:
            logger.critical(f"Error while retrieving user with Id={user_id}: {e}")
            return None
    

    async def get_id_by_telegram_id(self, db: AsyncSession, telegram_user_id: int) -> int | None:
        '''
        Returns the database ID of a user based on their telegram_user_id.
        '''
        try:
            user_id = await self.user_repo.get_id_by_telegram_id(db, telegram_user_id)
            logger.debug(f"Received user Id={user_id}")
            return user_id
        except Exception as e:
            logger.critical(f"Error while retrieving user Id with telegram Id={telegram_user_id}: {e}")
            return None

    
    async def update_last_article(self, db: AsyncSession, user_id: int, last_article_id: int) -> None:
        '''
        Updates the last_article_id for a given user.
        '''
        user_orm = await self.user_repo.get_by_id(db, user_id)
        if user_orm is not None:
            await self.user_repo.update_last_article(db, user_orm, last_article_id)
        