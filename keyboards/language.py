# keyboards/language.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORTED_LANGUAGES

def language_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("English", callback_data="set_lang_en"),
        InlineKeyboardButton("Русский", callback_data="set_lang_ru"),
        InlineKeyboardButton("Español", callback_data="set_lang_es")
    )
    return keyboard
