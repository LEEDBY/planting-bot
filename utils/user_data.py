# utils/user_data.py
import hashlib
from datetime import datetime

# Словарь для хранения опыта пользователей
user_xp = {}

# Словарь для хранения данных о посаженных деревьях
planted_trees = {}

# Словарь для хранения истории пожертвований с указанием времени
donation_history = {}

# Словарь для хранения языков пользователей
user_languages = {}

# Словарь для хранения реферальных данных
referrals = {}
planted_trees = {}

# Словарь для хранения статуса пользователей
user_sessions = {}

# Функция для проверки, есть ли у пользователя активная сессия
def has_started_session(user_id):
    return user_sessions.get(user_id, False)

# Функция для установки статуса сессии
def set_session_started(user_id):
    user_sessions[user_id] = True

# Функция для сброса статуса сессии
def reset_session_started(user_id):
    if user_id in user_sessions:
        user_sessions[user_id] = False

# Функция для записи пожертвований с указанной суммой и MEMO
async def record_donation(user_id, amount, memo):
    if user_id not in donation_history:
        donation_history[user_id] = []

    donation_history[user_id].append({
        'amount': amount,          # Сумма пожертвования
        'memo': memo,              # MEMO для отслеживания
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Время пожертвования
    })

    print(f"Пожертвование {amount} TON от пользователя {user_id} с MEMO {memo} записано в историю.")

# Добавляем пользователю XP
def add_xp(user_id, xp):
    if user_id in user_xp:
        user_xp[user_id] += xp
    else:
        user_xp[user_id] = xp

# Получаем текущее количество XP пользователя
def get_user_xp(user_id):
    return user_xp.get(user_id, 0)

def get_user_language(user_id):
    return user_languages.get(user_id, 'en')

def set_user_language(user_id, language_code):
    user_languages[user_id] = language_code


def plant_tree(user_id):
    # Обновляем общее количество посаженных деревьев
    if user_id in planted_trees:
        planted_trees[user_id] += 1
    else:
        planted_trees[user_id] = 1
        print(f"Пользователь {user_id} посадил {planted_trees[user_id]} деревьев.")

    # Добавляем запись в историю пожертвований с текущим временем
    if user_id not in donation_history:
        donation_history[user_id] = []
    
    donation_history[user_id].append({
        "amount": 1,  # Каждое пожертвование = 1 TON
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Время пожертвования
    })

def get_planted_trees(user_id):
    return planted_trees.get(user_id, 0)

def get_donation_history(user_id):
    return donation_history.get(user_id, [])

def generate_memo(user_id):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    memo_string = f"{user_id}_{current_time}"
    memo_hash = hashlib.sha256(memo_string.encode()).hexdigest()[:10]  # Берем 10 символов хеша
    return memo_hash

# Функция для подтверждения посадки дерева
async def confirm_plant_tree(user_id):
    # Обновляем количество посаженных деревьев для пользователя
    plant_tree(user_id)

    # Начисляем пользователю опыт
    add_xp(user_id, 10)

    print(f"Пользователь {user_id} посадил дерево. Добавлено 10 XP.")