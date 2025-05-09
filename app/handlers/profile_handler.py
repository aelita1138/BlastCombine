import asyncio
import os
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, InlineQuery, Message, Document, InlineKeyboardButton
from app.database.models import Account
from app.database.requests import add_account_for_user, create_stats, get_user_accounts_by_tg_id, get_user_by_tg_id
from app.keyboards.menu import generate_back_button

from pyrogram import Client

class AddAccount(StatesGroup):
    waiting_for_session_file = State()

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


@profile_router.inline_query(F.query == "my_profiles")
async def handler_my_profiles(inline_query: InlineQuery):
    accounts = await get_user_accounts_by_tg_id(tg_id=inline_query.from_user.id)
    accounts = accounts if accounts else []

    results = []

    # 🔹 Кнопка "Добавить аккаунт" всегда первая
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

    # 🔹 Если есть аккаунты — отобразить их
    if accounts:
        for account in accounts:
            results.append(
                InlineQueryResultArticle(
                    id=str(account.id),
                    title=f"{account.first_name} {account.last_name or ''}".strip(),
                    description=f"@{account.username}" if account.username else "Без username",
                    thumbnail_url="https://icon-library.com/images/my-account-icon/my-account-icon-24.jpg",
                    input_message_content=InputTextMessageContent(
                        message_text=f"Аккаунт: {account.first_name} @{account.username or '—'}"
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
    
    await inline_query.answer(results, cache_time=1)


# Новый хендлер: подробная информация об аккаунте по тексту "Аккаунт: ..."
@profile_router.message(F.text.startswith("Аккаунт: "))
async def show_account_info(message: Message):
    username = message.text.split("@")[-1].strip()
    accounts = await get_user_accounts_by_tg_id(tg_id=message.from_user.id)
    account = next((acc for acc in accounts if acc.username == username), None)

    if not account:
        await message.answer("Аккаунт не найден.")
        return

    stats = account.stats
    if not stats:
        await create_stats(account.id)
        accounts = await get_user_accounts_by_tg_id(tg_id=message.from_user.id)
        account = next((acc for acc in accounts if acc.username == username), None)
        stats = account.stats

    account_text = f"""
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

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧾 Открыть профиль", url=f"https://t.me/{account.username}")],
        [InlineKeyboardButton(text="🗑 Удалить аккаунт", callback_data=f"delete:{account.id}")],
        [InlineKeyboardButton(text="➕ Добавить прокси", switch_inline_query_current_chat=f"proxy:{account.id}")]
    ])

    await message.answer(account_text, parse_mode="HTML", reply_markup=keyboard)

@profile_router.message(F.text == "add new account")
async def cmd_add_account(message: Message, state: FSMContext):
    await message.answer("Отправь .session файл:")
    await state.set_state(AddAccount.waiting_for_session_file)


@profile_router.message(AddAccount.waiting_for_session_file, F.document)
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
