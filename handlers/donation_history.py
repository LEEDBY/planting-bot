from aiogram import types
from aiogram.dispatcher import Dispatcher
from utils.db import get_donation_history, get_user_language
from utils.localization import _

# Обработчик для истории пожертвований
async def donation_history_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)  # Асинхронно получаем язык пользователя

    # Получаем историю пожертвований пользователя из базы данных
    donations = await get_donation_history(user_id)

    if donations:
        # Если есть пожертвования, формируем сообщение с историей
        donation_history_message = _(lang_code, "donation_history_header") + "\n"
        for donation in donations:
            # donation[0] - это timestamp, donation[1] - amount
            donation_history_message += _(lang_code, "donation_entry", time=donation[0], amount=donation[1]) + "\n"
    else:
        # Если пожертвований нет, отправляем сообщение об отсутствии данных
        donation_history_message = _(lang_code, "no_donations_message")

    # Кнопка для возврата в главное меню
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu")
    )

    # Обновляем сообщение с историей пожертвований
    await callback_query.message.edit_text(donation_history_message, reply_markup=keyboard)
    await callback_query.answer()

# Функция для регистрации обработчика истории пожертвований
def register_donation_history_handler(dp: Dispatcher):
    dp.register_callback_query_handler(donation_history_handler, lambda c: c.data == "donation_history")
