# handlers/referral.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from utils.db import get_user_language, track_referral  # Исправлен импорт
from utils.localization import _
from utils.db_api import get_referral_link


async def referral_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)  # Теперь функция асинхронная
    
    referral_link = await get_referral_link(user_id)  # Асинхронный вызов
    referral_message = _(lang_code, "referral_message", referral_link=referral_link)
    
    # Кнопка для возврата в главное меню
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu")
    )

    # Обновляем сообщение с реферальной ссылкой
    await callback_query.message.edit_text(referral_message, reply_markup=keyboard)
    await callback_query.answer()

async def register_user_via_referral(user_id, referrer_id):
    conn = await connect_db()

    # Проверяем, является ли пользователь 1 уже рефералом пользователя 2
    async with conn.execute("""
        SELECT * FROM referrals WHERE user_id = ? AND referrer_id = ?
    """, (referrer_id, user_id)) as cursor:
        existing_referral = await cursor.fetchone()

    # Если реферал уже существует, не отправляем сообщение
    if existing_referral:
        print(f"[DEBUG] Пользователь {user_id} уже является рефералом пользователя {referrer_id}, сообщение не показывается.")
        await conn.close()
        return

    # Проверяем, существует ли уже обратная связь (referrer_id -> user_id)
    async with conn.execute("""
        SELECT * FROM referrals WHERE user_id = ? AND referrer_id = ?
    """, (user_id, referrer_id)) as cursor:
        reverse_referral = await cursor.fetchone()

    if reverse_referral:
        print(f"[DEBUG] Взаимные рефералы запрещены между {user_id} и {referrer_id}, сообщение не показывается.")
        await conn.close()
        return

    # Если проверки пройдены, добавляем нового реферала
    await track_referral(user_id, referrer_id)
    print(f"Новый пользователь {user_id} зарегистрирован через реферала {referrer_id}")

    # Отправляем приветственное сообщение только если реферал добавлен впервые
    await send_welcome_message(referrer_id, user_id)

    await conn.close()

def register_referral_handler(dp: Dispatcher):
    dp.register_callback_query_handler(referral_handler, lambda c: c.data == "invite_friend")
