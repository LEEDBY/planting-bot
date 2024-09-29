# keyboards/main_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.localization import _

def main_menu_keyboard(lang_code):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(_(lang_code, "main_menu.plant_tree"), callback_data="plant_tree"),
        InlineKeyboardButton(_(lang_code, "main_menu.profile"), callback_data="profile")
    )
    keyboard.add(
        InlineKeyboardButton(_(lang_code, "main_menu.raffle"), callback_data="raffle"),
        InlineKeyboardButton(_(lang_code, "main_menu.invite_friend"), callback_data="invite_friend")
    )
    keyboard.add(
        InlineKeyboardButton(_(lang_code, "main_menu.leaderboard"), callback_data="leaderboard_referrals"),
        InlineKeyboardButton(_(lang_code, "main_menu.donation_history"), callback_data="donation_history")
    )
    keyboard.add(
        InlineKeyboardButton(_(lang_code, "main_menu.change_language"), callback_data="change_language"),
        InlineKeyboardButton(_(lang_code, "main_menu.missions"), callback_data="missions")
    )
    return keyboard