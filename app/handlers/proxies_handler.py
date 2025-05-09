from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.proxies import generate_proxies_menu

proxies_router = Router()

my_proxies_text = """
📎Меню прокси

❗️Для управлением прокси, нажмите кнопку "Список прокси"
Перед вам откроется список прокси, с возможностью поиска и добавления новых прокси.
"""

@proxies_router.callback_query(F.data == "menu:proxies")
async def handler_proxies(query: CallbackQuery):
    await query.message.edit_text(text=my_proxies_text, reply_markup=await generate_proxies_menu())
