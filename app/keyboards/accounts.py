from app.keyboards.menu import generate_back_button
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def generate_accounts_menu():
    buttons = [
        [InlineKeyboardButton(text="💻 Список аккаунтов (0 шт.)", switch_inline_query_current_chat="my_profiles")],
        [InlineKeyboardButton(text="📂 Категории аккаунтов", callback_data="accounts:categories")],
        [InlineKeyboardButton(text="🔐 Установка 2FA", callback_data="accounts:2fa")],
        [InlineKeyboardButton(text="☠️ Завершить сторонние сессии", callback_data="accounts:terminate_sessions")],
        [InlineKeyboardButton(text="♻️ Переавторизация", callback_data="accounts:reauth")],
        [InlineKeyboardButton(text="🕶 Настройки приватности", callback_data="accounts:privacy")],
        [InlineKeyboardButton(text="⬇️ Скачать аккаунты", callback_data="accounts:download")],
        [InlineKeyboardButton(text="🧹 Массовое удаление", callback_data="accounts:bulk_delete")],
        [InlineKeyboardButton(text="🔁 Конвертер аккаунтов", callback_data="accounts:convert")],
        [InlineKeyboardButton(text="🧽 Чистка аккаунта", callback_data="accounts:clean")],
        [InlineKeyboardButton(text="📣 Авто-установка канала", callback_data="accounts:auto_channel")],
        [InlineKeyboardButton(text="👁 Статистика просмотров (переходники)", callback_data="accounts:view_stats")],
        [InlineKeyboardButton(text="🤓 Редактировать профили", callback_data="accounts:edit_profiles")],
        [InlineKeyboardButton(text="⚡️ Статистика комментариев", callback_data="accounts:comment_stats")],
        await generate_back_button("main_menu"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)