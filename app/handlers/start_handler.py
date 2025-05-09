from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.handlers.main_menu_handler import handler_main_menu_after_start
from app.database import requests

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    await requests.add_user(tg_id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name)
    
    await message.answer(text="💼")
    await handler_main_menu_after_start(message=message)

