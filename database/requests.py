
from database.models import async_session
from database.models import (User, FemaleCategory, FemaleItem,
                             MaleCategory, MaleItem,
                             ChildCategory, ChildItem)
from sqlalchemy import select # update, delete, add


async def set_user(tg_id):
    async with async_session() as session:  # Открываем сессию.
        user = await session.scalar(select(User).where(User.tg_id == tg_id))  # Запрашиваем id клиента.

        if not user:  # Добавляем клиента в базу, если его там нет.
            session.add(User(tg_id=tg_id, name=None, phone=None))  # Добавляем id клиента в базу.
            await session.commit()  # Сохраняем id клиента в базе.


async def get_female_categories():
    async with async_session() as session:  # Открываем сессию.
        return await session.scalars(select(FemaleCategory))  # Возвращаем все женские категории.

async def get_female_items(category_id):
    async with async_session() as session:  # Открываем сессию.
        return await session.scalars(select(FemaleItem).where(FemaleItem.category == category_id))  # Возвращаем все женские услуги.

async def get_female_item(item_id):
    async with async_session() as session:  # Открываем сессию.
        return await session.scalar(select(FemaleItem).where(FemaleItem.id == item_id))  # Возвращаем описание выбранной услуги.


async def get_male_categories():
    async with async_session() as session:  # Открываем сессию.
        return await session.scalars(select(MaleCategory))  # Возвращаем все мужские категории.

async def get_male_items(category_id):
    async with async_session() as session:  # Открываем сессию.
        return await session.scalars(select(MaleItem).where(MaleItem.category == category_id))  # Возвращаем все мужские услуги.

async def get_male_item(item_id):
    async with async_session() as session:  # Открываем сессию.
        return await session.scalar(select(MaleItem).where(MaleItem.id == item_id))  # Возвращаем описание выбранной услуги.


async def get_child_categories():
    async with async_session() as session:  # Открываем сессию.
        return await session.scalars(select(ChildCategory))  # Возвращаем все детские категории.

async def get_child_items(category_id):
    async with async_session() as session:  # Открываем сессию.
        return await session.scalars(select(ChildItem).where(ChildItem.category == category_id))  # Возвращаем все детские услуги.

async def get_child_item(item_id):
    async with async_session() as session:  # Открываем сессию.
        return await session.scalar(select(ChildItem).where(ChildItem.id == item_id))  # Возвращаем описание выбранной услуги.
