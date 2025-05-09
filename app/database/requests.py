from aiosqlite import IntegrityError
from sqlalchemy import select
from app.database.models import Account, AccountStats, async_session, User
from sqlalchemy.orm import selectinload


async def get_user_by_tg_id(tg_id: int) -> User | None:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()  # либо объект User, либо None
        return user

async def add_user(tg_id: int, username: str | None, first_name: str, last_name: str | None):
    if not await get_user_by_tg_id(tg_id=tg_id):
        async with async_session() as session:
            async with session.begin():
                user = User(
                    tg_id=tg_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_subscribed=False,
                    subscription_expires_at=None,
                )
                session.add(user)
            await session.commit()
        print("Пользователь добавлен!")


async def get_user_accounts_by_tg_id(tg_id: int) -> list[Account]:
    async with async_session() as session:
        result = await session.execute(
            select(User)
            .options(selectinload(User.accounts))
            .where(User.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()
        return user.accounts if user else []
    
    
async def add_account_for_user(
    user_id: int,
    account_tg_id: int,
    session_file: str,
    first_name: str,
    last_name: str | None = None,
    username: str | None = None,
):
    async with async_session() as session:
        try:
            async with session.begin():
                account = Account(
                    user_id=user_id,
                    account_tg_id=account_tg_id,
                    session_file=session_file,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=True
                )
                session.add(account)
            await session.commit()
            print("Аккаунт успешно добавлен.")
        except IntegrityError:
            print("❌ Ошибка: Такой session_file уже существует.")


async def create_stats(account_id):
    stats = AccountStats(account_id=account_id)
    async with async_session() as session:
        session.add(stats)
        await session.commit()