import json
from datetime import datetime

# Загрузка миссий из файла
def load_missions():
    with open('missions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Проверка выполнения ежедневных и еженедельных миссий
def check_missions(user_data):
    missions = load_missions()
    completed_missions = []

    # Проверка ежедневных миссий
    for mission in missions['daily_missions']:
        if mission['type'] == 'daily':
            if mission['id'] == 1 and user_data['trees'] >= 1:
                completed_missions.append(mission)
            elif mission['id'] == 2 and user_data['referrals'] >= 1:
                completed_missions.append(mission)

    # Проверка еженедельных миссий
    for mission in missions['weekly_missions']:
        if mission['type'] == 'weekly':
            if mission['id'] == 3 and user_data['trees'] >= 5:
                completed_missions.append(mission)
            elif mission['id'] == 4 and user_data['referrals'] >= 2:
                completed_missions.append(mission)

    return completed_missions

# Получение активных миссий для пользователя
def get_active_missions():
    missions = load_missions()
    active_missions = {
        "daily": missions['daily_missions'],
        "weekly": missions['weekly_missions']
    }
    return active_missions
