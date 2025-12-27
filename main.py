from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import asyncio
import logging
import asyncio
from sqlalchemy import text

from config import settings
from message_handler import router
import app.models  # noqa
from app.database.session import async_session
from app.repositories.article_repo import ArticleRepo
from app.repositories.user_article_repo import UserArticleRepo
from app.repositories.user_repo import UserRepo
from app.services.article_service import ArticleService
from app.services.user_service import UserService
from app.services.user_article_service import UserArticleService


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(settings.TELEGRAM_API_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def main():
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
