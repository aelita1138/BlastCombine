from app.keyboards.menu import generate_back_button
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def generate_new_task_menu():
    buttons = [
        [InlineKeyboardButton(text="👀Масслукинг", callback_data="new_task:masslooking")],
        [InlineKeyboardButton(text="📺Теггер в историях", callback_data="new_task:story_tagger")],
        [InlineKeyboardButton(text="🚀Инвайтинг", callback_data="new_task:inviting")],
        [InlineKeyboardButton(text="💼Парсинг", callback_data="new_task:parsing")],
        [InlineKeyboardButton(text="💬Комментинг", callback_data="new_task:commenting")],
        [InlineKeyboardButton(text="👥👥Клонирование чата", callback_data="new_task:cloning")],
        [InlineKeyboardButton(text="🔒 Вступление в чаты/каналы", callback_data="new_task:join_locked")],
        [InlineKeyboardButton(text="🔒 Тегер", callback_data="new_task:locked_tagger")],
        await generate_back_button("main_menu"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)