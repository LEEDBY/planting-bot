# handlers/start.py

import asyncio
from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.main_menu import main_menu_keyboard
from utils.localization import _  # Импортируем функцию локализации
from utils.user_data import has_started_session, set_session_started, reset_session_started  # Добавим функцию сброса сессии
from utils.db import add_user, connect_db, track_referral  # Импортируем функцию для добавления пользователя

# Время для сброса сессии (в секундах)
SESSION_TIMEOUT = 600  # 10 минут

async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    lang_code = message.from_user.language_code or 'en'

    # Добавляем пользователя в базу данных
    await add_user(user_id, first_name, lang_code)
    print(f"Пользователь {user_id} успешно добавлен.")  # Отладка
    
    # Проверяем, пришел ли пользователь по реферальной ссылке
    args = message.get_args()  # Получаем аргументы команды /start
    if args:
        try:
            referrer_id = int(args)  # Извлекаем ID реферера из аргументов
            if referrer_id != user_id:  # Проверка, что пользователь не ссылается сам на себя
                conn = await connect_db()  # Выполняем подключение к базе данных

                # Проверка, не является ли referrer_id уже рефералом user_id
                async with conn.execute("""
                    SELECT * FROM referrals WHERE user_id = ? AND referrer_id = ?
                """, (referrer_id, user_id)) as cursor:
                    reverse_referral = await cursor.fetchone()

                if reverse_referral:
                    print(f"[DEBUG] Взаимное добавление рефералов запрещено между {user_id} и {referrer_id}. Сообщение не показывается.")
                else:
                    # Проверяем, добавлен ли этот пользователь ранее как реферал
                    async with conn.execute("""
                        SELECT * FROM referrals WHERE user_id = ? AND referrer_id = ?
                    """, (user_id, referrer_id)) as cursor:
                        existing_referral = await cursor.fetchone()

                    if existing_referral:
                        print(f"[DEBUG] Пользователь {user_id} уже зарегистрирован как реферал у {referrer_id}. Сообщение не отправляется.")
                    else:
                        await track_referral(user_id, referrer_id)  # Добавляем реферала
                        await message.answer(_(lang_code, "registered_via_referral", referrer_id=referrer_id))

                await conn.close()  # Закрываем соединение с базой данных
        except ValueError:
            await message.answer(_(lang_code, "invalid_referral_link"))
    
    # Приветственное сообщение
    welcome_text = _(lang_code, "start_message", first_name=message.from_user.first_name)
    await message.answer(welcome_text, reply_markup=main_menu_keyboard(lang_code))

    # Отмечаем, что пользователь начал сессию
    set_session_started(user_id)

    # Запуск таймера для сброса сессии через SESSION_TIMEOUT
    await asyncio.sleep(SESSION_TIMEOUT)
    reset_session_started(user_id)

# Обработчик любого текстового сообщения от пользователя
async def start_menu_handler(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, есть ли у пользователя активная сессия
    if not has_started_session(user_id):
        # Если сессии нет, отправляем главное меню
        lang_code = message.from_user.language_code or 'en'
        keyboard = main_menu_keyboard(lang_code)
        
        # Отправляем главное меню
        await message.answer(_(lang_code, "welcome_main_menu"), reply_markup=keyboard)
        
        # Отмечаем, что пользователь начал сессию
        set_session_started(user_id)

        # Запуск таймера для сброса сессии
        await asyncio.sleep(SESSION_TIMEOUT)
        reset_session_started(user_id)
    else:
        # Если сессия уже была, можно обрабатывать как обычное сообщение
        await message.answer(_(lang_code, "use_main_menu"))

# Регистрация обработчиков
def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(start_menu_handler, content_types=types.ContentType.TEXT)  # Для любых сообщений
