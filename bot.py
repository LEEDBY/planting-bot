# bot.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import BOT_TOKEN
from handlers import register_handlers
from utils.localization import i18n
from utils.db import create_tables  # Импортируем функцию создания таблиц

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    # Создание таблиц перед запуском
    await create_tables()  # Добавляем создание таблиц

    # Добавление middleware для логирования и локализации
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(i18n)

    # Регистрация обработчиков
    register_handlers(dp)

    # Запуск бота
    try:
        await dp.start_polling()
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
