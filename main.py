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
        # Цель: 14:35 сегодня
        target_time = datetime.combine(now.date(), time(14, 35))
        if now >= target_time:
            # если уже позже 14:35, переносим на завтра
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)  # ждем до следующего 10 утра

        try:
            await bot.send_message(chat_id=450056320, text="Привет! Это сообщение в 10 утра")
        except Exception as e:
            logger.exception(f"Ошибка при отправке ежедневного сообщения: {e}")


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
    