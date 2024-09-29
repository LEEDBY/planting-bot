# handlers/leaderboard.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from utils.db import get_referral_leaderboard, get_tree_leaderboard, get_user_language  # Используем асинхронные функции
from utils.localization import _

# Асинхронная функция для создания текста лидерборда по рефералам
async def create_referral_leaderboard(lang_code):
    referrals = await get_referral_leaderboard()  # Асинхронно получаем данные из БД

    leaderboard_text = _(lang_code, "leaderboard_referral_header") + "\n"
    for idx, (user_id, count) in enumerate(referrals, start=1):
        user_name = f"{_(lang_code, 'user')} {user_id}"  # Локализуем "Пользователь"
        leaderboard_text += f"{idx}. {user_name} — {count} {_(lang_code, 'referrals')}\n"
    
    return leaderboard_text

# Асинхронная функция для создания текста лидерборда по деревьям
async def create_tree_leaderboard(lang_code):
    trees = await get_tree_leaderboard()  # Асинхронно получаем данные из БД

    leaderboard_text = _(lang_code, "leaderboard_tree_header") + "\n"
    for idx, (user_id, count) in enumerate(trees, start=1):
        user_name = f"{_(lang_code, 'user')} {user_id}"  # Локализуем "Пользователь"
        leaderboard_text += f"{idx}. {user_name} — {count} {_(lang_code, 'trees')}\n"
    
    return leaderboard_text

# Асинхронный обработчик для отображения лидерборда
async def leaderboard_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)  # Асинхронно берём язык из базы данных

    # Проверяем категорию, по которой был запрос (рефералы или деревья)
    category = callback_query.data.split('_')[-1]

    if category == "referrals":
        leaderboard_text = await create_referral_leaderboard(lang_code)
    elif category == "trees":
        leaderboard_text = await create_tree_leaderboard(lang_code)
    else:
        leaderboard_text = _(lang_code, "no_leaderboard_data")
    
    # Добавляем кнопки для переключения между категориями и возврата в меню
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(_(lang_code, "leaderboard_referral_button"), callback_data="leaderboard_referrals"),
        types.InlineKeyboardButton(_(lang_code, "leaderboard_tree_button"), callback_data="leaderboard_trees")
    ).add(
        types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu")
    )

    # Обновляем сообщение с выбранной категорией лидерборда
    await callback_query.message.edit_text(leaderboard_text, reply_markup=keyboard)
    await callback_query.answer()

def register_leaderboard_handler(dp: Dispatcher):
    # Обработка кнопок для различных категорий лидерборда
    dp.register_callback_query_handler(leaderboard_handler, lambda c: c.data.startswith('leaderboard_'))
