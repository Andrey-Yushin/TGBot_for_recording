
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


admin_router = Router()


@admin_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Панель администратора активна.')
