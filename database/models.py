
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'  # Название столбца

    id: Mapped[int] = mapped_column(primary_key=True)  # id услуги.
    tg_id = mapped_column(BigInteger)                  # Телеграмм id.
    name: Mapped[str] = mapped_column(String(50))      # Имя клиента.
    phone: Mapped[str] = mapped_column(String(11))     # Номер телефона.


class FemaleCategory(Base):
    __tablename__ = 'female_categories'  # Название столбца

    id: Mapped[int] = mapped_column(primary_key=True)  # id категории услуг.
    name: Mapped[str] = mapped_column(String(30))      # Название категории услуг.


class FemaleItem(Base):
    __tablename__ = 'female_items'  # Название столбца

    id: Mapped[int] = mapped_column(primary_key=True)      # id услуги.
    name: Mapped[str] = mapped_column(String(30))          # Название услуги.
    description: Mapped[str] = mapped_column(String(100))  # Описание услуги.
    price: Mapped[str] = mapped_column(String(16))         # Цена услуги.
    time: Mapped[str] = mapped_column(String(16))          # Время выполнениея услуги.
    category: Mapped[int] = mapped_column(ForeignKey('female_categories.id'))  # Категоия услуги.

class MaleCategory(Base):
    __tablename__ = 'male_categories'  # Название столбца

    id: Mapped[int] = mapped_column(primary_key=True)  # id категории услуг.
    name: Mapped[str] = mapped_column(String(30))      # Название категории услуг.


class MaleItem(Base):
    __tablename__ = 'male_items'  # Название столбца

    id: Mapped[int] = mapped_column(primary_key=True)      # id услуги.
    name: Mapped[str] = mapped_column(String(30))          # Название услуги.
    description: Mapped[str] = mapped_column(String(100))  # Описание услуги.
    price: Mapped[str] = mapped_column(String(16))         # Цена услуги.
    time: Mapped[str] = mapped_column(String(16))          # Время выполнениея услуги.
    category: Mapped[int] = mapped_column(ForeignKey('male_categories.id'))  # Категоия услуги.


class ChildCategory(Base):
    __tablename__ = 'child_categories'  # Название столбца

    id: Mapped[int] = mapped_column(primary_key=True)  # id категории услуг.
    name: Mapped[str] = mapped_column(String(30))      # Название категории услуг.


class ChildItem(Base):
    __tablename__ = 'child_items'  # Название столбца

    id: Mapped[int] = mapped_column(primary_key=True)      # id услуги.
    name: Mapped[str] = mapped_column(String(30))          # Название услуги.
    description: Mapped[str] = mapped_column(String(100))  # Описание услуги.
    price: Mapped[str] = mapped_column(String(16))         # Цена услуги.
    time: Mapped[str] = mapped_column(String(16))          # Время выполнениея услуги.
    category: Mapped[int] = mapped_column(ForeignKey('child_categories.id'))  # Категоия услуги.

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Создаем все таблицы.
