from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.new_task import generate_new_task_menu

new_task_router = Router()

my_new_task_text = """
💻 Инструменты для работы с телеграмом
"""

@new_task_router.callback_query(F.data == "menu:new_task")
async def handler_proxies(query: CallbackQuery):
    await query.message.edit_text(text=my_new_task_text, reply_markup=await generate_new_task_menu())
