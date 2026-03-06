
import os

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message

from settings.config import BOT_TOKEN, ADMIN_ID
import admin_panel.admin_keys as adminkey


admin_router = Router()
bot = Bot(token=BOT_TOKEN)

@admin_router.message(Command("admin"))
async def admin_start(message: Message):
    """Запускает панель администратора."""
    tg_id = message.from_user.id
    if tg_id == int(ADMIN_ID):
        await message.answer('Панель администратора активна.',
                            reply_markup=adminkey.admin_keys)



@admin_router.callback_query(F.data == 'send_all')
async def send_all(message: Message):
    await bot.send_message('Отправлено всем клиентам.')
