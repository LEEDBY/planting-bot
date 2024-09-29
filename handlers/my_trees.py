# handlers/my_trees.py

from aiogram import types
from aiogram.dispatcher import Dispatcher
from utils.user_data import get_planted_trees
from utils.localization import _

async def my_trees_handler(message: types.Message):
    user_id = message.from_user.id
    lang_code = message.from_user.language_code or 'en'
    
    # Получаем количество деревьев, посаженных пользователем
    trees_planted = get_planted_trees(user_id)
    
    # Формируем сообщение о количестве посаженных деревьев
    response_message = _(lang_code, "my_trees_message", trees_planted=trees_planted)
    await message.answer(response_message)

def register_my_trees_handler(dp: Dispatcher):
    dp.register_message_handler(my_trees_handler, lambda message: message.text == _(message.from_user.language_code or 'en', "main_menu.my_trees"))
