from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

import app.models  # noqa
from app.database.session import async_session
from app.repositories.user_repo import UserRepo
from app.services.user_service import UserService
from app.repositories.article_repo import ArticleRepo
from app.services.article_service import ArticleService
from app.repositories.user_article_repo import UserArticleRepo
from app.services.user_article_service import UserArticleService


router = Router()


def get_keyboard():
    # Set up keyboard
        keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Знаю"), KeyboardButton(text="Не знаю")],        
            [KeyboardButton(text="Слухати"), KeyboardButton(text="Вимовити")]
        ],
        resize_keyboard=True)
        return keyboard


@router.message(Command("start"))
async def start_command(message: Message):
    async with async_session() as db_session:
        user_article_service = UserArticleService(UserArticleRepo())

        telegram_user_id = message.from_user.id  # type: ignore
        telegram_user_name = message.from_user.username  # type: ignore
        telegram_first_name = message.from_user.first_name  # type: ignore
        telegram_last_name = message.from_user.last_name  # type: ignore
    
        # Check if user exist in the database
        user_service = UserService(UserRepo())
        current_user_id = await user_service.get_id_by_telegram_id(db_session, telegram_user_id)
        current_user = None
        if current_user_id is None:
            # Create new user it the database
            new_user = await user_service.create(db_session, 
                telegram_user_id = telegram_user_id, 
                telegram_user_name = telegram_user_name, 
                telegram_first_name = telegram_first_name, 
                telegram_last_name = telegram_last_name
                )        
            # Add user vocabulary to the new_user
            article_service = ArticleService(ArticleRepo())
            article_list = await article_service.get_all(db_session)
            await user_article_service.init_user_vocabulary(db_session, 
                user = new_user, 
                article_list = article_list
                )            
            current_user = new_user
        else:
            current_user = await user_service.get_by_id(db_session, current_user_id)
        
        if current_user is None:
            # Should never happen; added for type checker
            await message.answer("Помилка. Користувач не знайдений.")
            return
        
        keyboard = get_keyboard()
                
        if current_user.last_article is None:
            # If last_article is None get next article and save it to the user.last_article
            next_article = await user_article_service.get_next_article(db_session, current_user.id, last_article=None)
            await user_service.update_last_article(db_session, current_user.id, next_article.id)
            await message.answer(next_article.ukr_word)
            await message.answer(f"<tg-spoiler>{next_article.eng_word}</tg-spoiler>", parse_mode='HTML', reply_markup=keyboard)
        else:
            # Send user.last_article
            await message.answer(current_user.last_article.ukr_word)
            await message.answer(f"<tg-spoiler>{current_user.last_article.eng_word}</tg-spoiler>", parse_mode='HTML', reply_markup=keyboard)
        

async def handle_know(message: Message):
    await message.answer("Ви обрали: Знаю")
    return
    # TODO check if the user is_sync
    # TODO get next article and assign it to the last article
    telegram_user_id = message.from_user.id  # type: ignore
    async with async_session() as db_session:
        user_service = UserService(UserRepo())
        current_user_id = await user_service.get_id_by_telegram_id(db_session, telegram_user_id)
        if current_user_id is not None:
            user_last_article_id = await user_service.get_last_article_id_by_user_id(db_session, current_user_id)
            if user_last_article_id is not None:
                user_article_service = UserArticleService(UserArticleRepo())
                await user_article_service.update_weight(db_session, user_last_article_id, delta = -1)

            user_article_service = UserArticleService(UserArticleRepo())    
            next_article = await user_article_service.get_next_article(db_session, current_user_id, None)  
            await message.answer(next_article.ukr_word)
            await message.answer(f"<tg-spoiler>{next_article.eng_word}</tg-spoiler>", parse_mode='HTML')
            # TODO and assign it to the last article


async def handle_dont_know(message: Message):
    await message.answer("Ви обрали: Не знаю")


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
