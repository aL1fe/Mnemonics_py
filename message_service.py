from aiogram.types import Message
import logging

from app.database.session import async_session
from app.models.article import Article
from app.models.user import User
from app.services.user_service import UserService
from app.services.article_service import ArticleService
from app.services.user_article_service import UserArticleService
from app.repositories.user_repo import UserRepo
from app.repositories.article_repo import ArticleRepo
from app.repositories.user_article_repo import UserArticleRepo


logger = logging.getLogger(__name__)


class MessageService:
    def __init__(self):
        self.user_service = UserService(UserRepo())
        self.article_service = ArticleService(ArticleRepo())
        self.user_article_service = UserArticleService(UserArticleRepo())


    async def start(self, message: Message) -> Article | None:
        async with async_session() as db_session:
            async with db_session.begin():
                telegram_user_id = message.from_user.id  # type: ignore
                telegram_user_name = message.from_user.username  # type: ignore
                telegram_first_name = message.from_user.first_name  # type: ignore
                telegram_last_name = message.from_user.last_name  # type: ignore
            
                # Check if user exist in the database
                current_user_id = await self.user_service.get_id_by_telegram_id(db_session, telegram_user_id)
                current_user = None
                new_user_last_article = None
                if current_user_id is None:
                    # Create new user it the database
                    new_user = await self.user_service.create(db_session, 
                        telegram_user_id = telegram_user_id, 
                        telegram_user_name = telegram_user_name, 
                        telegram_first_name = telegram_first_name, 
                        telegram_last_name = telegram_last_name
                        )        
                    if new_user is None:
                        await message.answer("Помилка. Не вдалося створити користувача.")
                        return
                    
                    # Add user vocabulary to the new_user
                    article_list = await self.article_service.get_all(db_session)
                    if not article_list:
                        await message.answer("Помилка. Не знайти словник.")
                        return
                    await self.user_article_service.init_user_vocabulary(db_session, 
                        user = new_user, 
                        article_list = article_list
                        )
                    new_user.last_article = article_list[0]
                    current_user = new_user
                    await self.user_service.update_last_article(db_session, current_user.id, current_user.last_article.id) # type: ignore
                else:
                    # Get current user from the database
                    current_user = await self.user_service.get_by_id(db_session, current_user_id)
                if current_user is None:
                    # Should never happen; added for type checker
                    await message.answer("Помилка. Користувач не знайдений.")
                    return
                
                # Send user.last_article
                return current_user.last_article
            

    async def handle_article_feedback(self, message: Message, delta: int) -> Article | None:
        # TODO check if the user is_sync
        telegram_user_id = message.from_user.id  # type: ignore
        async with async_session() as db_session:
            async with db_session.begin():
                current_user_id = await self.user_service.get_id_by_telegram_id(db_session, telegram_user_id)
                if current_user_id is None:
                    # Should never happen; added for type checker
                    await message.answer("Помилка. Користувач не знайдений.")
                    return

                current_user = await self.user_service.get_by_id(db_session, current_user_id)        
                if current_user is None:
                    # Should never happen; added for type checker
                    await message.answer("Помилка. Користувач не знайдений.")
                    return
                
                last_article_id = current_user.last_article.id if current_user.last_article is not None else None
                if last_article_id is not None:
                    await self.user_article_service.update_weight(db_session, current_user_id, last_article_id, delta = delta)
    
                next_article = await self.user_article_service.get_next_article(db_session, current_user_id, current_user.last_article)
                if next_article is None:
                    await message.answer("Помилка. Не вдалося отримати наступну пару слiв.")
                    return
                await self.user_service.update_last_article(db_session, current_user.id, next_article.id)
                return next_article
