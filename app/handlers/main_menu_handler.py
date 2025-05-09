from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.keyboards.menu import generate_main_menu

main_menu_router = Router()

@main_menu_router.callback_query(F.data == "menu:main_menu")
async def handler_main_menu(query: CallbackQuery):
    text = "👋 Добро пожаловать, пользователь!"
    await query.message.edit_text(text=text, reply_markup=await generate_main_menu())

async def handler_main_menu_after_start(message: Message):
    text = "👋 Добро пожаловать, пользователь!"
    await message.answer(text=text, reply_markup=await generate_main_menu())