
import asyncio

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from settings.config import BOT_TOKEN, ADMIN_ID
import admin_panel.admin_keys as adminkey
import database.requests as rq

admin_router = Router()
bot = Bot(token=BOT_TOKEN)


class Notification(StatesGroup):
    text = State()


@admin_router.message(F.text.lower() == 'создать объявление 📢')
async def start_notification(message: Message, state: FSMContext):
    """Начало создания объявления."""
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("Введите объявление для рассылки:")
        await state.set_state(Notification.text)


@admin_router.message(Notification.text)
async def control_notification(message: Message, state: FSMContext, bot: Bot):
    """Проверяем объявление."""
    text=message.text  # Сохраняем введеный текст.

    # Ловим нажатие кнопок.
    if text.lower() in ['клиенты 👥', 'мои услуги 🛒', 'записи 📝']:
        if text.lower() == 'клиенты 👥':
            await clients_data(message)  # Вызываем функцию кнопки.
        elif text.lower() == 'мои услуги 🛒':
            await admin_service(message)
        elif text.lower() == 'записи 📝':
            await start_notification(message)
        return  # Ничего не возвращаем.

    await state.update_data(text=text)  # Вводим введеный текст в состояние.
    await message.answer(
        f"<b>Текст объявления:</b>\n{text}\n<b>Подтвердите отправку</b>",
        reply_markup=adminkey.notification_keys,
        parse_mode='HTML'
    )


@admin_router.callback_query(F.data == "send_notification")
async def send_notification(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Отправляет всем клиентам объявление."""
    users = await rq.get_users()
    # Проверяем наличие клиентов.
    if not users:
        await callback.answer("❌ Нет пользователей для рассылки.")
        await state.clear()
        return

    await callback.message.edit_text("⏳ Отправляю объявление...")

    data = await state.get_data()
    text = data["text"]

    # Отправляем сообщение клиентам.
    for user in users:
        try:
            # Проверяем что пользователь - клиент.
            if user.tg_id != int(ADMIN_ID):
                await bot.send_message(user.tg_id, text)
            # Задержка между сообщениями (30 сообщений в секунду максимум)
            await asyncio.sleep(0.05)
        except Exception as e:
            callback.message.asnswer(
                f"Ошибка отправки пользователю {user.tg_id}: {e}")

    await callback.message.edit_text("✅ Отправка завершена!")
    await state.clear()


@admin_router.callback_query(F.data == "cancel_notification")
async def send_notification(callback: CallbackQuery, state: FSMContext):
    """Отмена объявления."""
    await state.clear()  # Очистка состояния.
    await callback.message.delete()  # Удаляем сообщение.
    await callback.message.answer("✅ Объявление отменено.")
    await callback.answer()  # Заглушка для кнопки.


@admin_router.message(F.text.lower() == 'клиенты 👥')
async def clients_data(message: Message):
    """Выводит список клиентов."""
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("📋 Список клиентов:",
                            reply_markup=await adminkey.user_list())


@admin_router.callback_query(F.data.startswith('userlist_'))
async def page_client_list(callback: CallbackQuery):
    """Выводит следующую страницу списка клиентов."""
    await callback.answer()  # Заглушка для кнопки.
    start = int(callback.data.split('_')[1])  # Первый клиент в списке.
    end = int(callback.data.split('_')[2])  # Последний клиент в списке.
    await callback.message.edit_text('📋 Список клиентов',
        reply_markup=await adminkey.user_list(start, end))


@admin_router.callback_query(F.data.startswith('user_'))
async def user_info(callback: CallbackQuery):
    """Выводит следующую страницу списка клиентов."""
    await callback.answer()  # Заглушка для кнопки.
    tg_id = int(callback.data.split('_')[1])
    user = await rq.get_user_info(tg_id)
    if user:
        user_reg = user.date_created  # Дата создание.
        user_reg = user_reg.strftime("%d.%m.%Y")  # Формат отображения даты.
        await callback.message.edit_text(
            f"<b>Имя:</b> {user.name}\n"
            f"<b>Номер телефона:</b> {user.phone}\n"
            f"<b>Дата регистрации: {user_reg}</b>",
            reply_markup= await adminkey.back_client_list(user.tg_id),
            parse_mode='HTML')


@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_client(callback: CallbackQuery):
    tg_id = callback.data.split('_')[1]
    user = await rq.get_user_info(tg_id)
    await callback.message.edit_text(
        f'Действительно удалить: {user.name}?',
        reply_markup=await adminkey.delete_user(tg_id)
    )

@admin_router.callback_query(F.data.startswith('accept_delete_'))
async def delete_client(callback: CallbackQuery):
    tg_id = callback.data.split('_')[2]
    await rq.delete_user(tg_id)  # Удаляем клиента из базы.
    # Удаляем подтверждение в чате об удалении клиента.
    await callback.message.delete()
    await callback.message.answer('Клиент удален ✅')  # Отпрвляем оповещение.
    await callback.message.answer('📋 Список клиентов',
        reply_markup=await adminkey.user_list())


@admin_router.message(F.text.lower() == 'записи 📝')
async def start_notification(message: Message):
    """Выводит список записей."""
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("📝 Список записей:")


@admin_router.message(F.text.lower() == 'мои услуги 🛒')
async def admin_service(message: Message):
    """Выводит услуги."""
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("📋 Список услуг.",
                    reply_markup=await adminkey.service_list())
