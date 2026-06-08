from datetime import datetime, time, timedelta
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


async def daily_message():
    while True:
        now = datetime.now()
        # Target every day at 12:35
        target_time = datetime.combine(now.date(), time(12, 35))
        if now >= target_time:
            # If it's already after 12:35 PM, we'll reschedule it for tomorrow
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)  # Wait until 12:35 PM
 
        try:
            await bot.send_message(chat_id=450056320, text="Привіт! Давай повторимо декілька слів.")
        except Exception as e:
            logger.exception(f"Error sending daily message: {e}")

        await asyncio.sleep(60)


async def main():
    asyncio.create_task(daily_message())

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


# alembic revision --autogenerate -m "message"
 