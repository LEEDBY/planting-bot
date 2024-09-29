import asyncio
from aiogram import Dispatcher
from config import TON_WALLET_ADDRESS, DONATION_AMOUNT, CHECK_EXPIRATION_TIME, MIN_DONATION_AMOUNT, PAYMENT_CHECK_INTERVAL
from aiogram import types
from keyboards.main_menu import main_menu_keyboard
from utils.ton_api import check_payment
from utils.user_data import generate_memo
from utils.localization import _  # Импортируем функцию локализации
from utils.db import record_donation, confirm_plant_tree, get_user_language

# Глобальный словарь для отслеживания статуса платежей
payment_status = {}

# Функция для отправки чека с ожиданием платежа
async def send_payment_invoice(callback_query: types.CallbackQuery, user_id, memo):
    wallet_address = TON_WALLET_ADDRESS
    amount = DONATION_AMOUNT
    lang_code = await get_user_language(user_id)
    payment_message = (
        _(lang_code, "plant_tree_header") + "\n\n"
        + _(lang_code, "payment_message", amount=amount, wallet_address=wallet_address, memo=memo, expiration_time=CHECK_EXPIRATION_TIME)
    )

    # Логируем процесс генерации MEMO и отправки инвойса
    print(f"[DEBUG] Генерация MEMO для пользователя {user_id}: {memo}")
    
    # Кнопки "Подтвердить платеж", "Отменить" и "Главное меню"
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(_(lang_code, "confirm_payment_button"), callback_data=f"confirm_payment_{memo}"),
        types.InlineKeyboardButton(_(lang_code, "cancel_payment_button"), callback_data=f"cancel_payment_{memo}")
    )

    # Обновляем старое сообщение с чеком
    await callback_query.message.edit_text(payment_message, reply_markup=keyboard, parse_mode="Markdown")

    # Инициализация статуса платежа (не отменён)
    payment_status[user_id] = False

# Обработчик для подтверждения платежа (запускаем проверку сразу после подтверждения)
async def confirm_payment_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    memo = callback_query.data.split('_')[-1]
    lang_code = await get_user_language(user_id)

    # Логируем процесс подтверждения платежа
    print(f"[DEBUG] Подтверждение платежа для пользователя {user_id}, MEMO: {memo}")

    # Отправляем сообщение с ожиданием платежа и кнопкой "Главное меню"
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu")
    )
    await callback_query.message.edit_text(_(lang_code, "confirming_payment_message"), reply_markup=keyboard)

    # Асинхронная проверка транзакций с использованием интервала из конфига
    asyncio.create_task(wait_for_payment(callback_query, memo))

# Функция для асинхронной проверки платежа с использованием PAYMENT_CHECK_INTERVAL
async def wait_for_payment(callback_query, memo):
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)

    # Проверка платежа в течение указанного времени
    for i in range(int(CHECK_EXPIRATION_TIME * 60 / PAYMENT_CHECK_INTERVAL)):  # Количество проверок
        payment = await check_payment(memo)

        if payment:
            amount_received = int(payment['amount']) / 1e9  # Конвертируем из нанотонов в TON
            amount_received = round(amount_received, 2)  # Округляем до 2 знаков после запятой

            # Логируем получение успешного платежа
            print(f"[DEBUG] Платеж найден с MEMO: {memo}, сумма: {amount_received} TON")

            # Записываем пожертвование в любом случае
            await record_donation(user_id, amount_received)
            print(f"[DEBUG] Пользователь {user_id} сделал пожертвование: {amount_received} TON")

            # Сравниваем с минимальной суммой пожертвования
            if amount_received >= MIN_DONATION_AMOUNT:
                # Если сумма достаточная, сажаем дерево
                await confirm_plant_tree(user_id)

                # Логируем процесс посадки дерева
                print(f"[DEBUG] Пользователь {user_id} посадил дерево")

                # Кнопки после успешного платежа
                keyboard = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu"),
                    types.InlineKeyboardButton(_(lang_code, "plant_another_tree_button"), callback_data="plant_tree")
                )
                await callback_query.message.edit_text(
                    _(lang_code, "payment_confirmed_message", amount_received=amount_received),
                    reply_markup=keyboard
                )
            else:
                # Если сумма меньше минимальной, отправляем благодарность и записываем в историю
                await record_donation(user_id, amount_received, memo)

                # Логируем запись пожертвования
                print(f"[DEBUG] Пользователь {user_id} сделал пожертвование: {amount_received} TON")

                # Кнопки после частичного платежа
                keyboard = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu")
                )
                await callback_query.message.edit_text(
                    _(lang_code, "thank_you_donation_message", amount_received=amount_received, min_donation=MIN_DONATION_AMOUNT),
                    reply_markup=keyboard
                )
            return

        await asyncio.sleep(PAYMENT_CHECK_INTERVAL)  # Интервал ожидания перед следующей проверкой

    # Если по истечении времени платеж не был найден
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(_(lang_code, "back_to_menu_button"), callback_data="main_menu")
    )
    await callback_query.message.edit_text(_(lang_code, "payment_not_found_message"), reply_markup=keyboard)

# Обработчик для кнопки "Главное меню"
async def back_to_menu_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang_code = await get_user_language(user_id)
    keyboard = main_menu_keyboard(lang_code)
    
    # Отправляем главное меню
    await callback_query.message.edit_text(_(lang_code, "return_to_main_menu"), reply_markup=keyboard)
    await callback_query.answer()

# Функция для отмены платежа
async def cancel_payment_handler(callback_query: types.CallbackQuery):
    memo = callback_query.data.split('_')[-1]
    await cancel_payment(callback_query, callback_query.from_user.id, memo)
    await callback_query.message.edit_text(_(await get_user_language(callback_query.from_user.id), "payment_cancelled_message"))
    await callback_query.answer()

async def cancel_payment(callback_query: types.CallbackQuery, user_id, memo):
    # Обновляем статус, что платеж отменён
    payment_status[user_id] = True
    
    # Логика отмены платежа (например, удаление его из очереди или базы данных)
    await callback_query.bot.send_message(user_id, _(await get_user_language(user_id), "memo_cancelled", memo=memo))
    
    # Отправляем главное меню после отмены
    lang_code = await get_user_language(user_id)
    keyboard = main_menu_keyboard(lang_code)
    await callback_query.bot.send_message(user_id, _(lang_code, "return_to_main_menu"), reply_markup=keyboard)

# Обработчик для кнопки "Посадить дерево"
async def plant_tree_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Генерируем уникальный MEMO для платежа
    memo = generate_memo(user_id)

    # Обновляем сообщение с чеком для оплаты
    await send_payment_invoice(callback_query, user_id, memo)

    await callback_query.answer()
