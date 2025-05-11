import asyncio
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery,  InlineQueryResultArticle, InputTextMessageContent, InlineQuery, Message, Document, InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards.accounts import generate_account_profile_menu, generate_accounts_menu
from app.database.requests import add_account_for_user, create_stats, get_user_accounts_by_tg_id, get_user_by_tg_id
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.database.models import Account
from pyrogram import Client

class AddAccount(StatesGroup):
    waiting_for_session_file = State()

accounts_router = Router()


@accounts_router.callback_query(F.data == "menu:accounts")
async def handler_accounts(query: CallbackQuery):
    text = """
👤Меню аккаунтов

❗️Для добавления и удаления аккаунтов, пожалуйста, нажмите "Список аккаунтов"

Перед вам откроется список аккаунтов с возможностью поиска по названию, имени или ID.

➕ Для добавления новых аккаунтов - нажмите кнопку сверху в выпадающем меню

🚮 Для удаления аккаунта - нажмите на него в выпадающем меню, после чего бот пришлёт подтверждение.
"""
    await query.message.edit_text(text=text, reply_markup=await generate_accounts_menu())

@accounts_router.inline_query(F.query == "accounts:list")
async def handler_my_accounts(inline_query: InlineQuery):
    accounts = await get_user_accounts_by_tg_id(tg_id=inline_query.from_user.id)
    results = [] # Сюда сохраняем список аккаунтов и навигационные кнопки

    results.append(
        InlineQueryResultArticle(
            id="add_account",
            title="➕ Добавить аккаунт",
            description="Нажми, чтобы добавить аккаунт.",
            thumbnail_url="https://icon-library.com/images/my-account-icon/my-account-icon-24.jpg",
            input_message_content=InputTextMessageContent(
                message_text="add new account"
            )
        )
    )

    if accounts:
        for account in accounts:
            print(account)
            print(account.account_tg_id)
            results.append(
                InlineQueryResultArticle(
                    id=str(account.id),
                    title=f"{account.first_name} {account.last_name or ''}".strip(),
                    description=f"@{account.username}" if account.username else "Без username",
                    thumbnail_url="https://icon-library.com/images/my-account-icon/my-account-icon-24.jpg",
                    input_message_content=InputTextMessageContent(
                        message_text=f"show account: {account.account_tg_id}"
                    )
                )
            )
    else:
        results.append(
            InlineQueryResultArticle(
                id="no_accounts",
                title="У тебя ещё нет аккаунтов...",
                description="Добавь свой первый Telegram-аккаунт",
                thumbnail_url="https://icon-library.com/images/my-account-icon/my-account-icon-24.jpg",
                input_message_content=InputTextMessageContent(
                    message_text="add new account"
                )
            )
        )
    
    await inline_query.answer(results, cache_time=0)


def get_account(tg_id: int, accounts):
    return next((account for account in accounts if account.account_tg_id == tg_id), None)

async def get_account_stats(tg_id: int, message):
    accounts = await get_user_accounts_by_tg_id(tg_id=message.from_user.id)
    account = get_account(tg_id, accounts)
    
    if not account:
        return None, None

    if not account.stats:
        await create_stats(account_id=account.id)
        accounts = await get_user_accounts_by_tg_id(tg_id=message.from_user.id)
        account = get_account(tg_id, accounts)

    return account.stats, account


@accounts_router.message(F.text.startswith("show account:"))
async def show_account_info(message: Message):
    tg_id = int(message.text.split(":")[1].strip(""))
    stats, account = await get_account_stats(tg_id=tg_id, message=message)
            
    text = f"""
👨‍💻 <b>Информация об аккаунте</b>
├ <b>ID:</b> {account.account_tg_id}
├ <b>Имя и фамилия:</b> {account.first_name} {account.last_name or ''}
├ <b>Телефон:</b> Недоступно
├ <b>Username:</b> @{account.username or "—"}
├ <b>Премиум:</b> Нет
├ <b>Прокси:</b> {account.proxy_string if account.proxy_host else "Нет"}
└ <b>Добавлен:</b> {account.created_at.strftime('%d.%m.%Y') if account.created_at else "—"}

💬 <b>Статистика рассылок:</b>
├ За сегодня: {stats.mailing_today} шт.
├ За месяц: {stats.mailing_month} шт.
└ За всё время: {stats.mailing_total} шт.

📢 <b>Статистика комментариев:</b>
├ За сегодня: {stats.comments_today} шт.
├ За месяц: {stats.comments_month} шт.
└ За всё время: {stats.comments_total} шт.

💌 <b>Статистика отметок в сторис:</b>
├ За сегодня: {stats.story_tags_today} шт.
├ За месяц: {stats.story_tags_month} шт.
└ За всё время: {stats.story_tags_total} шт.

📢 <b>Статистика просмотров сторис:</b>
├ За сегодня: {stats.stories_viewed_today} шт.
├ За месяц: {stats.stories_viewed_month} шт.
└ За всё время: {stats.stories_viewed_total} шт.

💕 <b>Статистика реакций на сторис:</b>
├ За сегодня: {stats.story_reactions_today} шт.
├ За месяц: {stats.story_reactions_month} шт.
└ За всё время: {stats.story_reactions_total} шт.

📲 <b>Статистика инвайта:</b>
├ За сегодня: {stats.invites_today} шт.
├ За месяц: {stats.invites_month} шт.
└ За всё время: {stats.invites_total} шт.
"""
    await message.answer(text=text, parse_mode="HTML", reply_markup=await generate_account_profile_menu(account))


@accounts_router.message(F.text == "add new account")
async def cmd_add_account(message: Message, state: FSMContext):
    await message.answer("Отправь .session файл:")
    await state.set_state(AddAccount.waiting_for_session_file)


@accounts_router.message(AddAccount.waiting_for_session_file, F.document)
async def handle_session_file(message: Message, state: FSMContext):
    file = message.document
    if not file.file_name.endswith(".session"):
        await message.answer("Это не .session файл.")
        return

    tg_id = message.from_user.id
    session_dir = f"app/sessions/{tg_id}"
    os.makedirs(session_dir, exist_ok=True)

    file_path = f"{session_dir}/{file.file_name}"

    await message.bot.download(file, destination=file_path)

    try:
        app = Client(
            name=file.file_name.replace(".session", ""),
            api_id=os.getenv("API_ID"),
            api_hash=os.getenv("API_HASH"),
            workdir=session_dir
        )
        await app.start()
        me = await app.get_me()

        user = await get_user_by_tg_id(tg_id=message.from_user.id)
        await add_account_for_user(
            user_id=user.id,
            account_tg_id=me.id,
            session_file=file_path,
            first_name=me.first_name,
            last_name=me.last_name,
            username=me.username
        )

        await app.stop()
        await message.answer(f"✅ Аккаунт {me.id} | {me.first_name} добавлен.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
        try:
            await app.stop()
        except:
            pass
    await state.clear()
