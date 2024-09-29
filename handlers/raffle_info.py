# handlers/raffle_info.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from utils.localization import _
from utils.db import get_user_language

async def raffle_info_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)
    
    # Информационное сообщение о розыгрыше призов
    raffle_info_message = _(lang_code, "raffle_info_message")
    # Кнопка для возврата в главное меню
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu")
    )

    # Обновляем сообщение с информацией о розыгрыше
    await callback_query.message.edit_text(raffle_info_message, reply_markup=keyboard)
    await callback_query.answer()

def register_raffle_info_handler(dp: Dispatcher):
    dp.register_callback_query_handler(raffle_info_handler, lambda c: c.data == "raffle")