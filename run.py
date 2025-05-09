import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers import (
    start_handler, 
    main_menu_handler, 
    profile_handler,
    accounts_handler,
    proxies_handler,
    new_task_handler,
    )
from app.database.models import engine, Base

async def create_table_in_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def start_bot(bot: Bot, dp: Dispatcher):
    await create_table_in_database()
    await bot.send_message(chat_id=os.getenv("ADMIN"), text="Бот был запущен!")
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    routers = (
        start_handler.start_router,
        main_menu_handler.main_menu_router,
        profile_handler.profile_router,
        accounts_handler.accounts_router,
        proxies_handler.proxies_router,
        new_task_handler.new_task_router,

    )

    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_routers(*routers)
    asyncio.run(start_bot(bot=bot, dp=dp))