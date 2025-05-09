from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.accounts import generate_accounts_menu

accounts_router = Router()

my_accounts_text = """
👤Меню аккаунтов

❗️Для добавления и удаления аккаунтов, пожалуйста, нажмите "Список аккаунтов"

Перед вам откроется список аккаунтов с возможностью поиска по названию, имени или ID.

➕ Для добавления новых аккаунтов - нажмите кнопку сверху в выпадающем меню

🚮 Для удаления аккаунта - нажмите на него в выпадающем меню, после чего бот пришлёт подтверждение.
"""

@accounts_router.callback_query(F.data == "menu:accounts")
async def handler_accounts(query: CallbackQuery):
    await query.message.edit_text(text=my_accounts_text, reply_markup=await generate_accounts_menu())
