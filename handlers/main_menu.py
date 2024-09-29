# handlers/main_menu.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.main_menu import main_menu_keyboard
from utils.db import get_user_language  # Импортируем функцию из базы данных
from utils.localization import _  # Не забудь импортировать функцию локализации

# Асинхронный обработчик для главного меню
async def main_menu_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)  # Асинхронно получаем язык из базы данных
    
    # Обновляем главное меню с локализацией
    await callback_query.message.edit_text(_(lang_code, "hedder_menu"), reply_markup=main_menu_keyboard(lang_code))
    await callback_query.answer()

# Регистрация обработчика для главного меню
def register_main_menu_handler(dp: Dispatcher):
    dp.register_callback_query_handler(main_menu_handler, lambda c: c.data == "main_menu")
