from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.missions import get_active_missions, check_missions  # Эти функции можно обновить, если они берут данные из БД
from utils.db import get_planted_trees, get_referrals, get_user_language  # Получаем данные из БД
from utils.localization import _

async def missions_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)  # Асинхронно получаем язык из базы данных

    # Получаем активные миссии
    active_missions = get_active_missions()

    # Получаем данные пользователя из базы данных
    user_data = {
        'trees': await get_planted_trees(user_id),  # Асинхронно получаем количество деревьев
        'referrals': len(await get_referrals(user_id))  # Асинхронно получаем количество рефералов
    }

    # Проверяем, какие миссии выполнены
    completed_missions = check_missions(user_data)

    # Формируем сообщение о миссиях
    missions_message = _(lang_code, "active_missions_title") + "\n\n"
    
    # Ежедневные миссии
    missions_message += _(lang_code, "daily_missions") + ":\n"
    for mission in active_missions['daily']:
        status = "✅" if mission in completed_missions else "❌"
        missions_message += f"{status} {mission['title']} - {mission['description']}\n"

    # Еженедельные миссии
    missions_message += "\n" + _(lang_code, "weekly_missions") + ":\n"
    for mission in active_missions['weekly']:
        status = "✅" if mission in completed_missions else "❌"
        missions_message += f"{status} {mission['title']} - {mission['description']}\n"

    # Кнопка для возврата в главное меню
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu")
    )

    # Обновляем сообщение, без кнопки обновления
    await callback_query.message.edit_text(missions_message, reply_markup=keyboard)
    await callback_query.answer()

def register_missions_handler(dp: Dispatcher):
    dp.register_callback_query_handler(missions_handler, lambda c: c.data == "missions")
