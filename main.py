from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import asyncio
import logging

from config import settings
from message_handler import router


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(settings.TELEGRAM_API_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def main():
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
