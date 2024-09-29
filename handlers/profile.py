# profile.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db import get_planted_trees, get_user_xp, get_referrals, get_user_language  # Обновляем импорт на асинхронные функции
from utils.levels import get_level_by_xp
from utils.localization import _
from utils.achievements import get_user_achievements_with_progress

async def profile_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Логируем получение языка пользователя
    print(f"[DEBUG] Запрос языка для пользователя {user_id}")
    lang_code = await get_user_language(user_id)  # Асинхронно получаем язык
    print(f"[DATA] Язык пользователя {user_id}: {lang_code}")

    # Логируем получение данных профиля
    print(f"[DEBUG] Запрос данных профиля для пользователя {user_id}")

    # Получаем XP пользователя
    print(f"[DEBUG] Получение XP для пользователя {user_id}")
    xp = await get_user_xp(user_id)  # Асинхронно получаем XP
    print(f"[DATA] XP пользователя {user_id}: {xp}")

    # Вычисляем уровень пользователя на основе XP
    print(f"[DEBUG] Вычисление уровня для пользователя {user_id} на основе XP: {xp}")
    level = get_level_by_xp(xp)  # Эта функция, скорее всего, синхронная
    print(f"[DATA] Уровень пользователя {user_id}: {level}")

    # Получаем данные о посаженных деревьях
    print(f"[DEBUG] Получение данных о посаженных деревьях для пользователя {user_id}")
    trees = await get_planted_trees(user_id)  # Асинхронно получаем данные о деревьях
    print(f"[DATA] Количество деревьев пользователя {user_id}: {trees}")

    # Получаем количество рефералов
    print(f"[DEBUG] Получение рефералов для пользователя {user_id}")
    referrals = len(await get_referrals(user_id))  # Асинхронно получаем количество рефералов
    print(f"[DATA] Количество рефералов пользователя {user_id}: {referrals}")

    # Данные пользователя для проверки достижений
    user_data = {
        'trees': trees,
        'referrals': referrals
    }

    # Получаем достижения с прогрессом
    print(f"[DEBUG] Получение достижений с прогрессом для пользователя {user_id}")
    achievements_by_category = get_user_achievements_with_progress(user_data)
    print(f"[DATA] Достижения пользователя {user_id}: {achievements_by_category}")

    # Формируем сообщение профиля
    print(f"[DEBUG] Формирование сообщения профиля для пользователя {user_id}")
    profile_message = _(lang_code, "profile_message",
                        level=level,
                        xp=xp,
                        trees=trees,
                        referrals=referrals)
    
    # Добавляем категории достижений
    for category, achievements in achievements_by_category.items():
        profile_message += f"\n\n📋 {category}:\n"
        for achievement in achievements:
            profile_message += f"{achievement['icon']} {achievement['title']}: {achievement['progress']} ({achievement['percent']}%)\n"

    # Логируем окончание формирования сообщения профиля
    print(f"[DEBUG] Сообщение профиля для пользователя {user_id} сформировано успешно.")

    # Кнопка для возврата в главное меню
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu")
    )

    # Обновляем сообщение профиля
    print(f"[DEBUG] Обновление сообщения профиля для пользователя {user_id}")
    await callback_query.message.edit_text(profile_message, reply_markup=keyboard)
    await callback_query.answer()

    print(f"[DEBUG] Обработчик профиля завершил работу для пользователя {user_id}")

def register_profile_handler(dp: Dispatcher):
    dp.register_callback_query_handler(profile_handler, lambda c: c.data == "profile")
