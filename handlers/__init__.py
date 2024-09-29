# handlers/__init__.py

from aiogram.dispatcher import Dispatcher
from .start import register_start_handler
from .language import register_language_handler
from .referral import register_referral_handler
from .leaderboard import register_leaderboard_handler
from .tree import confirm_payment_handler, cancel_payment_handler, plant_tree_handler
from .profile import register_profile_handler  # Новый обработчик профиля
from .donation_history import donation_history_handler  # Новый импорт
from .raffle_info import register_raffle_info_handler  # Новый обработчик для информации о розыгрыше
from .missions import register_missions_handler  # Новый обработчик
from .main_menu import register_main_menu_handler  # Добавляем обработчик главного меню


def register_handlers(dp: Dispatcher):
    register_start_handler(dp)
    register_language_handler(dp)
    register_referral_handler(dp)
    register_leaderboard_handler(dp)
    register_profile_handler(dp)  # Регистрируем обработчик профиля
    register_raffle_info_handler(dp)  # Регистрируем обработчик информации о розыгрыше
    register_missions_handler(dp)  # Регистрируем обработчик миссий
    register_main_menu_handler(dp)  # Регистрируем обработчик главного меню
    dp.register_callback_query_handler(confirm_payment_handler, lambda c: c.data.startswith('confirm_payment_'))
    dp.register_callback_query_handler(cancel_payment_handler, lambda c: c.data.startswith('cancel_payment_'))
    dp.register_callback_query_handler(donation_history_handler, lambda c: c.data == "donation_history")  # Новый обработчик
    dp.register_callback_query_handler(plant_tree_handler, lambda c: c.data == "plant_tree")  # Обработчик для кнопки "Посадить дерево"