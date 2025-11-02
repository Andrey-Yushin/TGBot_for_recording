
import asyncio
import logging

from aiogram import Bot, Dispatcher
from user_panel.user_hand import user_router
from admin_panel.admin_hand import admin_router
from settings.config import BOT_TOKEN
from database.models import async_main


async def main():
    await async_main()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(user_router, admin_router)  # Обработка хэндлеров.
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Включаем логирование.
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен.')
