# handlers/language.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.language import language_keyboard
from utils.localization import _, SUPPORTED_LANGUAGES
from utils.db import get_user_language, set_user_language  # Импортируем функции работы с БД
from keyboards.main_menu import main_menu_keyboard

async def change_language_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)
    
    # Отображаем клавиатуру для выбора языка
    await callback_query.message.edit_text(_(lang_code, "choose_language"), reply_markup=language_keyboard())
    await callback_query.answer()

async def set_language_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang_code = callback_query.data.split('_')[-1]

    # Проверяем, поддерживается ли язык
    if lang_code in SUPPORTED_LANGUAGES:
        # Устанавливаем язык для пользователя
        await set_user_language(user_id, lang_code)
        await callback_query.message.edit_text(_(lang_code, "language_set"), reply_markup=main_menu_keyboard(lang_code))
    else:
        await callback_query.answer("Язык не поддерживается")

def register_language_handler(dp: Dispatcher):
    dp.register_callback_query_handler(change_language_handler, lambda c: c.data == "change_language")
    dp.register_callback_query_handler(set_language_callback, lambda c: c.data.startswith('set_lang_'))
