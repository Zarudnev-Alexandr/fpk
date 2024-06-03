from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Film(Base):
    __tablename__ = 'film'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(String(150), nullable=False)


class BotUser(Base):
    __tablename__ = 'user'

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    fio: Mapped[str]
    username: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)


class SubscribeChannel(Base):
    __tablename__ = 'subscribe_channel'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    link: Mapped[str]

