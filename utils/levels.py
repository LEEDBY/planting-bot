# utils/levels.py

import json

# Загрузка конфигурации уровней
def load_levels():
    with open('levels.json', 'r', encoding='utf-8') as f:
        return json.load(f)['levels']

# Получение текущего уровня пользователя на основе XP
def get_level_by_xp(xp):
    levels = load_levels()
    current_level = 0
    for level in levels:
        if xp >= level['xp_required']:
            current_level = level['level']
        else:
            break
    return current_level

# Получение информации о следующем уровне
def get_next_level_info(xp):
    levels = load_levels()
    for level in levels:
        if xp < level['xp_required']:
            return level
    return None  # Если пользователь достиг максимального уровня
