from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import logging

from app.services.message_service import MessageService


logger = logging.getLogger(__name__)
router = Router()


def get_keyboard() -> ReplyKeyboardMarkup:
    # Set up keyboard
        keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Знаю"), KeyboardButton(text="Не знаю")],        
            [KeyboardButton(text="Слухати"), KeyboardButton(text="Вимовити")]
        ],
        resize_keyboard=True)
        return keyboard


async def sync_user_vocabulary(user_id: int) -> None:
    pass


@router.message(Command("start"))
async def start_command(message: Message):
    keyboard = get_keyboard()

    message_service = MessageService()
    article = await message_service.start(message)
    if article is None: return # Should never happen; added for type checker

    await message.answer(article.ukr_word)
    await message.answer(f"<tg-spoiler>{article.eng_word}</tg-spoiler>", parse_mode='HTML', reply_markup=keyboard)
    

async def handle_know(message: Message):
    message_service = MessageService()
    next_article = await message_service.handle_article_feedback(message, delta=-1)
    if next_article is None: return # Should never happen; added for type checker

    await message.answer(next_article.ukr_word)
    await message.answer(f"<tg-spoiler>{next_article.eng_word}</tg-spoiler>", parse_mode='HTML')


async def handle_dont_know(message: Message):
    message_service = MessageService()
    next_article = await message_service.handle_article_feedback(message, delta=+1)
    await message.answer(next_article.ukr_word)  # type: ignore
    await message.answer(f"<tg-spoiler>{next_article.eng_word}</tg-spoiler>", parse_mode='HTML')  # type: ignore


async def handle_listen(message: Message):
    await message.answer("Ви обрали: Слухати")


async def handle_pronounce(message: Message):
    await message.answer("Ви обрали: Вимовити")


@router.message(F.text.in_(["Знаю", "Не знаю", "Слухати", "Вимовити"]))
async def handle_keyboard_response(message: Message):
    text = message.text
    handlers = {
        "Знаю": handle_know,
        "Не знаю": handle_dont_know,
        "Слухати": handle_listen,
        "Вимовити": handle_pronounce
    }
    
    if text in handlers:
        await handlers[text](message)
    else:
        await message.answer(f"Ви обрали: {text}")


@router.message()
async def handle_other_messages(message: Message):
    '''Processing all other messages'''
    await message.answer(f"Ви написали: {message.text}")
