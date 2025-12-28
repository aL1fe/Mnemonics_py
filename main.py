from aiogram import Bot, Dispatcher
import asyncio
import logging

from config import settings
from message_handler import router
from app.utils.logging_config import setup_logging


listener = setup_logging()
logger = logging.getLogger(__name__)

TOKEN = settings.TELEGRAM_API_TOKEN
bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def main():
    logger.info(f"Start bot with token = {TOKEN[:5]}")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Bot stopped with exception: {e}")
    finally:
        listener.stop()
        await bot.session.close()
    

if __name__ == "__main__":
    asyncio.run(main())
    