from app.keyboards.menu import generate_back_button
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def generate_proxies_menu():
    buttons = [
        [InlineKeyboardButton(text="🔌 Список прокси (0 шт.)", switch_inline_query_current_chat="proxy_list")],
        [InlineKeyboardButton(text="💻 Прикрепленные прокси", callback_data="proxy:attached")],
        [InlineKeyboardButton(text="🧷 Прикрепление к аккаунтам", callback_data="proxy:bind_accounts")],
        await generate_back_button("main_menu"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)