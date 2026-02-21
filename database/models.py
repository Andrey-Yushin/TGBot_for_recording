
from datetime import datetime

from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import pytz

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'  # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True)  # id клиента.
    tg_id = mapped_column(BigInteger)  # Телеграмм id.
    # Имя клиента.
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    # Номер телефона.
    phone: Mapped[str] = mapped_column(String(11), nullable=True)
    date_created: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(pytz.timezone('Europe/Moscow')),
        nullable=False
    )


class Services(Base):
    __tablename__ = 'services' # Название таблицы.

    id: Mapped[int] = mapped_column(primary_key=True)  # id услуги.
    tg_id = mapped_column(BigInteger)  # Телеграмм id.
    client_name: Mapped[str] = mapped_column(String(50), nullable=True)
    client_phone: Mapped[str] = mapped_column(String(11), nullable=True)
    # Дополнительный комментарий клиента.
    user_comment: Mapped[str] = mapped_column(String(50))
    # Название категории.
    service_category: Mapped[str] = mapped_column(String(50), nullable=True)
    # Название услуги.
    service_item: Mapped[str] = mapped_column(String(50), nullable=True)
    # Цена услуги.
    price: Mapped[str] = mapped_column(String(16), nullable=False)
    # Время услуги.
    time: Mapped[str] = mapped_column(String(16), nullable=False)


class Events(Base):
    __tablename__ = 'events'  # Название таблицы.

    id: Mapped[int] = mapped_column(primary_key=True)  # id акции.
    # Название акции.
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))  # Описание акции.
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # Цена акции.
    # Время выполнения акции.
    time: Mapped[str] = mapped_column(String(16), nullable=False)


class FemaleCategory(Base):
    __tablename__ = 'female_categories'  # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True)  # id категории услуг.
    # Название категории услуг.
    name: Mapped[str] = mapped_column(String(30), nullable=False)


class FemaleItem(Base):
    __tablename__ = 'female_items'  # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True)  # id услуги.
    # Название услуги.
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))  # Описание услуги.
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # Цена услуги.
    # Время выполнениея услуги.
    time: Mapped[str] = mapped_column(String(16), nullable=False)
    # Категоия услуги.
    category: Mapped[int] = mapped_column(ForeignKey('female_categories.id'))


class MaleCategory(Base):
    __tablename__ = 'male_categories'  # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True)  # id категории услуг.
    # Название категории услуг.
    name: Mapped[str] = mapped_column(String(30), nullable=False)


class MaleItem(Base):
    __tablename__ = 'male_items'  # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True)  # id услуги.
    # Название услуги.
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))  # Описание услуги.
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # Цена услуги.
    # Время выполнениея услуги.
    time: Mapped[str] = mapped_column(String(16), nullable=False)
    # Категоия услуги.
    category: Mapped[int] = mapped_column(ForeignKey('male_categories.id'))


class ChildCategory(Base):
    __tablename__ = 'child_categories'  # Название таблицы.

    id: Mapped[int] = mapped_column(primary_key=True)  # id категории услуг.
    # Название категории услуг.
    name: Mapped[str] = mapped_column(String(30), nullable=False)


class ChildItem(Base):
    __tablename__ = 'child_items'  # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True)  # id услуги.
    # Название услуги.
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100))  # Описание услуги.
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # Цена услуги.
    # Время выполнениея услуги.
    time: Mapped[str] = mapped_column(String(16), nullable=False)
    # Категоия услуги.
    category: Mapped[int] = mapped_column(ForeignKey('child_categories.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Создаем все таблицы.
