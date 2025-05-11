from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from app.keyboards.menu import generate_back_button


profile_router = Router()

my_profile_text = """
Общая информация:
📇 Идентификатор пользователя: 7628273384
💳 Статус подписки: Отсутствует
🔐 2FA пароль: 0

- Статистика за всё время:
👥 Загружено аккаунтов в бота: 0 шт.
➕ Заинвайчено пользователей: 0 шт.
📺 Опубликовано историй: 0 шт.
📩 Отмечено пользователей: 0 шт.
💬 Оставлено комментариев: 0 шт.
👀 Просмотрено историй: 0 шт.
❤️ Поставлено реакций на истории: 0 шт.
🛠 Выполнено различных задач: 0 шт.

- Статистика загруженных аккаунтов:
🚀 Валидные: 0 шт.
🟢 В работе: 0 шт.
☠️ Нерабочие: 0 шт.
🚫 Спам-блок: 0 шт.

👥 Заинвайчено с аккаунтов: 0 раз
💬 Оставлено комментариев: 0 шт.
📺 Опубликовано историй: 0 шт.
📩 Отмечено пользователей: 0 шт.
👀 Просмотрено историй: 0 шт.
❤️ Поставлено реакций на истории: 0 шт.
"""

@profile_router.callback_query(F.data == "menu:profile")
async def handler_my_profile(query: CallbackQuery):
    await query.message.edit_text(text=my_profile_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[await generate_back_button("main_menu")]))
