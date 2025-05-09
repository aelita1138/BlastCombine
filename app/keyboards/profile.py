from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def generate_profile_menu():
    buttons = [
        [InlineKeyboardButton(text="👤 Профиль", callback_data="menu:profile")],
        [
            InlineKeyboardButton(text="💻 Аккаунты", callback_data="menu:accounts"),
            InlineKeyboardButton(text="🔗 Прокси", callback_data="menu:proxies")
        ],
        [
            InlineKeyboardButton(text="🗓 Мои задачи", callback_data="menu:my_tasks"),
            InlineKeyboardButton(text="🗞 Новая задача", callback_data="menu:new_task")
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)