from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Integer, String, Boolean

DATABASE_URL = "sqlite+aiosqlite:///app/database/database.db"
engine = create_async_engine(url=DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    accounts = relationship("Account", back_populates="user", lazy="selectin")


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_tg_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    session_file: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    proxy_host: Mapped[str | None] = mapped_column(String, nullable=True)
    proxy_port: Mapped[int | None] = mapped_column(Integer, nullable=True)
    proxy_login: Mapped[str | None] = mapped_column(String, nullable=True)
    proxy_password: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="accounts", lazy="selectin")

    stats = relationship("AccountStats", uselist=False, back_populates="account", lazy="selectin")

    @property
    def proxy_string(self) -> str:
        if self.proxy_host and self.proxy_port:
            if self.proxy_login and self.proxy_password:
                return f"socks5://{self.proxy_login}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}"
            return f"socks5://{self.proxy_host}:{self.proxy_port}"
        return "Нет"


class AccountStats(Base):
    __tablename__ = "account_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), unique=True)

    # Рассылки
    mailing_today: Mapped[int] = mapped_column(Integer, default=0)
    mailing_month: Mapped[int] = mapped_column(Integer, default=0)
    mailing_total: Mapped[int] = mapped_column(Integer, default=0)

    # Комментарии
    comments_today: Mapped[int] = mapped_column(Integer, default=0)
    comments_month: Mapped[int] = mapped_column(Integer, default=0)
    comments_total: Mapped[int] = mapped_column(Integer, default=0)

    # Отметки в сторис
    story_tags_today: Mapped[int] = mapped_column(Integer, default=0)
    story_tags_month: Mapped[int] = mapped_column(Integer, default=0)
    story_tags_total: Mapped[int] = mapped_column(Integer, default=0)

    # Просмотры сторис
    stories_viewed_today: Mapped[int] = mapped_column(Integer, default=0)
    stories_viewed_month: Mapped[int] = mapped_column(Integer, default=0)
    stories_viewed_total: Mapped[int] = mapped_column(Integer, default=0)

    # Реакции на сторис
    story_reactions_today: Mapped[int] = mapped_column(Integer, default=0)
    story_reactions_month: Mapped[int] = mapped_column(Integer, default=0)
    story_reactions_total: Mapped[int] = mapped_column(Integer, default=0)

    # Инвайты
    invites_today: Mapped[int] = mapped_column(Integer, default=0)
    invites_month: Mapped[int] = mapped_column(Integer, default=0)
    invites_total: Mapped[int] = mapped_column(Integer, default=0)

    # Связь с аккаунтом
    account = relationship("Account", back_populates="stats", lazy="selectin")
