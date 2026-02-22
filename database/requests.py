
from database.models import async_session
from database.models import (User, Services,
                             FemaleCategory, FemaleItem,
                             MaleCategory, MaleItem,
                             ChildCategory, ChildItem)
from sqlalchemy import select, update, delete


async def set_user(tg_id):
    """Добавляет клиента в базу."""
    async with async_session() as session:  # Открываем сессию.
        user = await session.scalar(select(User).where(
            User.tg_id == tg_id))  # Запрашиваем id клиента.

        if not user:  # Добавляем клиента в базу, если его там нет.
            # Добавляем id клиента в базу.
            session.add(User(tg_id=tg_id, name=None, phone=None))
            await session.commit()  # Сохраняем id клиента в базе.


async def add_user(name, phone):
    """Добавляет информацию о клиенте в базу."""
    async with async_session() as session:  # Открываем сессию.
        # создаем объект пользователя.
        new_user = User(name=name, phone=phone)
        session.add(new_user)  # Добавляем клиента в базу.
        await session.commit()  # Применяем изменения
        return new_user


# Достаем информацию о клиенте
async def get_user_info(tg_id):
    """Получает информацию о клиенте."""
    async with async_session() as session:  # Открываем сессию.
        return await session.scalar(select(User).where(
            User.tg_id == tg_id))  # Возвращаем информацию о клиенте.


async def add_service(
        tg_id, client_name, client_phone, user_comment,
        service_category, service_item, price, time):
    """Добавляет услугу в базу."""
    async with async_session() as session:  # Открываем сессию.
        # создаем объект услуги.
        new_service = Services(
            tg_id=tg_id,
            client_name=client_name,
            client_phone=client_phone,
            user_comment=user_comment,
            service_category=service_category,
            service_item=service_item,
            price = price,
            time = time
        )
        session.add(new_service)  # Добавляем услугу в базу.
        await session.commit()  # Применяем изменения
        return new_service


async def update_user(tg_id, name, phone):
    """Обновляем имя и номер клиента."""
    async with async_session() as session:  # Открываем сессию.
        request = update(User).where(User.tg_id == tg_id).values(
            name=name,
            phone=phone
        )
        await session.execute(request)  # Отправляем запрос.
        await session.commit()  # Применяем изменения.
        return True  # Возвращаем информацию о клиенте.


async def update_name(tg_id, name):
    """Обновляет имя клиента."""
    async with async_session() as session:  # Открываем сессию.
        request = update(User).where(User.tg_id == tg_id).values(
            name=name
        )
        await session.execute(request)  # Отправляем запрос.
        await session.commit()  # Применяем изменения.
        return True


async def update_phone(tg_id, phone):
    """Обновляет номер клиента."""
    async with async_session() as session:  # Открываем сессию.
        request = update(User).where(User.tg_id == tg_id).values(
            phone=phone
        )
        await session.execute(request)  # Отправляем запрос.
        await session.commit()  # Применяем изменения.
        return True


async def update_comment(new_comment, id):
    """Обновляет комментарий услуги."""
    async with async_session() as session:  # Открываем сессию.
        request = update(Services).where(Services.id == id).values(
            user_comment=new_comment
        )
        await session.execute(request)  # Отправляем запрос.
        await session.commit()  # Применяем изменения.
        return True



async def delete_user(tg_id):
    """Удаляет клиента."""
    async with async_session() as session:  # Открываем сессию.
        # Обновляем данные клиента.
        request = delete(User).where(User.tg_id == tg_id)
        await session.execute(request)  # Отправляем запрос.
        await session.commit()  # Применяем изменения.
        return True

async def delete_service(service_id):
    """Удаляет запись от клиента."""
    async with async_session() as session:  # Открываем сессию.
        # Обновляем данные клиента.
        request = delete(Services).where(Services.id == service_id)
        await session.execute(request)  # Отправляем запрос.
        await session.commit()  # Применяем изменения.
        return True


async def get_user_services(tg_id):
    """Возвращает клиенту его записи."""
    async with async_session() as session:  # Открываем сессию.
        return await session.scalars(select(Services).where(
            Services.tg_id == tg_id))


async def get_service_info(service_id):
    """Возвращает все записи."""
    async with async_session() as session:  # Открываем сессию.
        return await session.scalar(select(Services).where(
            Services.id == service_id))


async def get_female_categories():
    """Возвращает все женские категории."""
    async with async_session() as session:  # Открываем сессию.
        return await session.scalars(select(FemaleCategory))

async def get_female_items(category_id):
    """Возвращает все женские услуги."""
    async with async_session() as session:  # Открываем сессию.
        return await session.scalars(select(FemaleItem
                            ).where(FemaleItem.category == category_id))

async def get_female_item(item_id):
    """Возвращает информацию по выбранной услуге."""
    async with async_session() as session:  # Открываем сессию.
        return await session.scalar(select(FemaleItem
                            ).where(FemaleItem.id == item_id))

async def get_female_category(category_id):
    """Возвращает категорию по id."""
    async with async_session() as session:  # Открываем сессию.
        return await session.scalar(select(FemaleCategory
                            ).where(FemaleCategory.id == category_id))


async def get_male_categories():
    async with async_session() as session:  # Открываем сессию.
        # Возвращаем все мужские категории.
        return await session.scalars(select(MaleCategory))

async def get_male_items(category_id):
    async with async_session() as session:  # Открываем сессию.
        # Возвращаем все мужские услуги.
        return await session.scalars(select(MaleItem).where(
            MaleItem.category == category_id))

async def get_male_item(item_id):
    async with async_session() as session:  # Открываем сессию.
        # Возвращаем описание выбранной услуги.
        return await session.scalar(select(MaleItem).where(
            MaleItem.id == item_id))

async def get_male_category(category_id):
    """Возвращает категорию по id."""
    async with async_session() as session:  # Открываем сессию.
        return await session.scalar(select(MaleCategory
                            ).where(MaleCategory.id == category_id))


async def get_child_categories():
    async with async_session() as session:  # Открываем сессию.
        # Возвращаем все детские категории.
        return await session.scalars(select(ChildCategory))

async def get_child_items(category_id):
    async with async_session() as session:  # Открываем сессию.
        # Возвращаем все детские услуги.
        return await session.scalars(select(ChildItem).where(
            ChildItem.category == category_id))

async def get_child_item(item_id):
    async with async_session() as session:  # Открываем сессию.
        # Возвращаем описание выбранной услуги.
        return await session.scalar(select(ChildItem).where(
            ChildItem.id == item_id))

async def get_child_category(category_id):
    """Возвращает категорию по id."""
    async with async_session() as session:  # Открываем сессию.
        return await session.scalar(select(ChildCategory
                            ).where(ChildCategory.id == category_id))
