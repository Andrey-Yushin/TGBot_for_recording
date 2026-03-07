
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

@admin_router.message(Command("admin"))
async def admin_start(message: Message):
    """Запускает панель администратора."""
    tg_id = message.from_user.id
    if tg_id == int(ADMIN_ID):
        await message.answer('Панель администратора активна.',
                            reply_markup=adminkey.admin_keys)


class Notification(StatesGroup):
    text = State()


@admin_router.message(F.text.lower() == 'создать объявление 📢')
async def start_notification(message: Message, state: FSMContext):
    """Начало создания объявления."""
    if message.from_user.id:
        await message.answer("Введите объявление для рассылки:")
        await state.set_state(Notification.text)


@admin_router.message(Notification.text)
async def control_notification(message: Message, state: FSMContext, bot: Bot):
    """Проверяем объявление."""
    text=message.text  # Сохраняем введеный текст.

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
    if message.from_user.id:
        await message.answer("📋 Список клиентов:")


@admin_router.message(F.text.lower() == 'мои услуги 🛒')
async def start_notification(message: Message):
    """Выводит услуги."""
    if message.from_user.id:
        await message.answer("📋 Меню редактирования услуг.")


@admin_router.message(F.text.lower() == 'записи 📝')
async def start_notification(message: Message):
    """Выводит список записей."""
    if message.from_user.id:
        await message.answer("📝 Список записей:")
