import json

# Загрузка достижений из файла конфигурации
def load_achievements():
    with open('achievements.json', 'r', encoding='utf-8') as f:
        return json.load(f)['achievements']

# Получение достижений пользователя с прогрессом
def get_user_achievements_with_progress(user_data):
    achievements = load_achievements()
    categorized_achievements = {
        "Посадка деревьев": [],
        "Приглашение друзей": []
    }

    for achievement in achievements:
        condition = achievement['condition']
        progress = 0
        if condition['type'] == 'trees':
            progress = min(user_data['trees'], condition['value'])
            percent = int((progress / condition['value']) * 100)
            categorized_achievements["Посадка деревьев"].append({
                "title": achievement['title'],
                "icon": "🌳",
                "progress": f"{progress}/{condition['value']} деревьев",
                "percent": percent
            })
        elif condition['type'] == 'referrals':
            progress = min(user_data['referrals'], condition['value'])
            percent = int((progress / condition['value']) * 100)
            categorized_achievements["Приглашение друзей"].append({
                "title": achievement['title'],
                "icon": "🏆",
                "progress": f"{progress}/{condition['value']} друзей",
                "percent": percent
            })
    
    return categorized_achievements
