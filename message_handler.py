from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command


router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    """Обработка команды /start"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Англійська", callback_data='english')],
        [InlineKeyboardButton(text="Нiмецька", callback_data='german')],
        [InlineKeyboardButton(text="Французька", callback_data='french')]
    ])
    
    await message.answer(
        "Оберіть мову для вивчення:", 
        reply_markup=keyboard
    )


@router.callback_query(F.data.in_(['english', 'german', 'french']))
async def handle_language_selection(callback: CallbackQuery):
    """Обработка выбора языка"""
    await callback.answer()
    
    button_texts = {
        'english': 'англійську',
        'german': 'німецьку', 
        'french': 'французьку',
    }
    
    selected = button_texts.get(callback.data, callback.data)
    await callback.message.edit_text(
        f"Чудово ви обрали для <tg-spoiler>вивчення</tg-spoiler> <b>{selected}</b> мову", 
        parse_mode='HTML'
    )


@router.message(Command("keyboard"))
async def start_with_keyboard(message: Message):
    """Показать клавиатуру с опциями"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Знаю"), KeyboardButton(text="Не знаю")],        
            [KeyboardButton(text="Слухати"), KeyboardButton(text="Вимовити")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "Обери дію:",
        reply_markup=keyboard
    )


# Отдельные функции-обработчики
async def handle_know(message: Message):
    """Обработка кнопки 'Знаю'"""
    user_id = message.from_user.id
    username = message.from_user.username or "Неизвестный"
    
    await message.answer(f"Пользователь {username} (ID: {user_id}) выбрал: Знаю")


async def handle_dont_know(message: Message):
    """Обработка кнопки 'Не знаю'"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔴 Сложное", callback_data='difficult'),
            InlineKeyboardButton(text="🟡 Среднее", callback_data='medium')
        ],
        [InlineKeyboardButton(text="🟢 Легкое", callback_data='easy')]
    ])
    
    await message.answer(
        "Насколько сложное это слово?", 
        reply_markup=keyboard
    )


async def handle_listen(message: Message):
    """Обработка кнопки 'Слухати'"""
    await message.answer("Ви обрали: Слухати")


async def handle_pronounce(message: Message):
    """Обработка кнопки 'Вимовити'"""
    await message.answer("Ви обрали: Вимовити")


@router.callback_query(F.data.in_(['difficult', 'medium', 'easy']))
async def handle_difficulty_selection(callback: CallbackQuery):
    """Обработка выбора сложности"""
    await callback.answer()
    
    difficulty_texts = {
        'difficult': '🔴 Сложное',
        'medium': '🟡 Среднее',
        'easy': '🟢 Легкое'
    }
    
    selected = difficulty_texts.get(callback.data, callback.data)
    await callback.message.edit_text(f"Вы выбрали: {selected}")


@router.message(F.text.in_(["Знаю", "Не знаю", "Слухати", "Вимовити"]))
async def handle_keyboard_response(message: Message):
    """Универсальный обработчик клавиатурных кнопок"""
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
    """Обработка всех остальных сообщений"""
    await message.answer(f"Ви написали: {message.text}")
