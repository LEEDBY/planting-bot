import sqlite3
import aiosqlite


async def create_tables():
    async with aiosqlite.connect('database.db') as db:
        # Таблица пользователей
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            language_code TEXT DEFAULT 'en',
            trees_planted INTEGER DEFAULT 0,
            referrals INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 0
        );
        """)
        print("[DEBUG] Таблица 'users' создана или уже существует.")

        # Создание таблицы прогресса по миссиям
        await db.execute("""
        CREATE TABLE IF NOT EXISTS user_missions (
            user_id INTEGER,
            mission_id TEXT,
            progress INTEGER DEFAULT 0,
            status TEXT DEFAULT 'in_progress',
            PRIMARY KEY (user_id, mission_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """)
        print("[DEBUG] Таблица 'user_missions' создана или уже существует.")

        # Создание таблицы прогресса по достижениям
        await db.execute("""
        CREATE TABLE IF NOT EXISTS user_achievements (
            user_id INTEGER,
            achievement_id TEXT,
            progress INTEGER DEFAULT 0,
            status TEXT DEFAULT 'in_progress',
            PRIMARY KEY (user_id, achievement_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """)
        print("[DEBUG] Таблица 'user_achievements' создана или уже существует.")

        # Создание таблицы для истории пожертвований
        await db.execute("""
        CREATE TABLE IF NOT EXISTS donation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """)
        print("[DEBUG] Таблица 'donation_history' создана или уже существует.")

        # Создание таблицы рефералов
        await db.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            user_id INTEGER,
            referrer_id INTEGER,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (referrer_id) REFERENCES users(user_id)
        );
        """)
        print("[DEBUG] Таблица 'referrals' создана или уже существует.")

        # Подтверждение изменений
        await db.commit()
        print("[DEBUG] Таблицы успешно созданы и изменения сохранены.")

# Подключение к базе данных SQLite (файл базы данных создается автоматически)
async def connect_db():
    # Открываем соединение с базой данных и создаём таблицы
    await create_tables()  # Здесь вызов функции должен быть без аргументов
    print("[DEBUG] Подключение к базе данных установлено.")
    return await aiosqlite.connect('database.db')

# Функция для добавления нового пользователя
async def add_user(user_id, first_name, language_code):
    conn = await connect_db()
    async with conn.execute("""
        INSERT INTO users (user_id, first_name, language_code)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO NOTHING
    """, (user_id, first_name, language_code)):
        await conn.commit()
    await conn.close()
    print(f"[DEBUG] Пользователь {user_id} добавлен в базу данных.")

# Функция для обновления прогресса миссии пользователя
async def update_mission_progress(user_id, mission_id, progress_increment):
    conn = await connect_db()
    async with conn.execute("""
        UPDATE user_missions
        SET progress = progress + ?
        WHERE user_id = ? AND mission_id = ?
    """, (progress_increment, user_id, mission_id)):
        await conn.commit()
    await conn.close()
    print(f"Mission {mission_id} progress updated for user {user_id}.")

    # Проверяем, выполнена ли миссия (например, сравниваем прогресс с нужным значением)
    async with conn.execute("""
        UPDATE user_missions
        SET status = 'completed'
        WHERE user_id = ? AND mission_id = ? AND progress >= (
            SELECT value FROM missions WHERE mission_id = ?
        )
    """, (user_id, mission_id, mission_id)):
        await conn.commit()

    await conn.close()

# Функция для получения истории пожертвований пользователя
async def get_donation_history(user_id):
    conn = await connect_db()
    async with conn.execute("""
        SELECT timestamp, amount FROM donation_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,)) as cursor:
        donations = await cursor.fetchall()
    await conn.close()
    return donations

    # Форматируем данные для дальнейшего использования
    return [{"timestamp": donation[0], "amount": donation[1]} for donation in donations]

# Функция для записи пожертвования в базу данных
async def record_donation(user_id, amount):
    conn = await connect_db()
    async with conn.execute("""
        INSERT INTO donation_history (user_id, amount, timestamp)
        VALUES (?, ?, datetime('now'))
    """, (user_id, amount)):
        await conn.commit()
    await conn.close()

# Асинхронная функция для получения языка пользователя
async def get_user_language(user_id):
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("""
            SELECT language_code FROM users WHERE user_id = ?
        """, (user_id,)) as cursor:
            result = await cursor.fetchone()
    return result[0] if result else 'en'

# Асинхронная функция для установки языка пользователя
async def set_user_language(user_id, lang_code):
    async with aiosqlite.connect('database.db') as db:
        await db.execute("""
            UPDATE users SET language_code = ? WHERE user_id = ?
        """, (lang_code, user_id))
        await db.commit()

# Асинхронная функция для получения данных реферального лидерборда
async def get_referral_leaderboard():
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("""
            SELECT user_id, referrals FROM users ORDER BY referrals DESC LIMIT 10
        """) as cursor:
            referrals = await cursor.fetchall()
    return referrals

# Асинхронная функция для получения данных лидерборда по деревьям
async def get_tree_leaderboard():
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("""
            SELECT user_id, trees_planted FROM users ORDER BY trees_planted DESC LIMIT 10
        """) as cursor:
            trees = await cursor.fetchall()
    return trees

# Функция для получения количества деревьев пользователя
async def get_planted_trees(user_id):
    conn = await connect_db()
    async with conn.execute("""
        SELECT trees_planted FROM users WHERE user_id = ?
    """, (user_id,)) as cursor:
        result = await cursor.fetchone()
    await conn.close()
    return result[0] if result else 0

# Функция для получения списка рефералов пользователя
async def get_referrals(user_id):
    async with aiosqlite.connect('database.db') as db:
        async with db.execute("""
            SELECT referrer_id FROM referrals WHERE user_id = ?
        """, (user_id,)) as cursor:
            referrals = await cursor.fetchall()
    return [referral[0] for referral in referrals] if referrals else []

# Функция для получения XP пользователя
async def get_user_xp(user_id):
    conn = await connect_db()
    async with conn.execute("""
        SELECT xp FROM users WHERE user_id = ?
    """, (user_id,)) as cursor:
        result = await cursor.fetchone()
    await conn.close()
    return result[0] if result else 0

# Функция для обновления количества деревьев
async def confirm_plant_tree(user_id):
    conn = await connect_db()

    # Увеличиваем количество деревьев
    async with conn.execute("""
        UPDATE users
        SET trees_planted = trees_planted + 1
        WHERE user_id = ?
    """, (user_id,)):
        await conn.commit()
        print(f"[DEBUG] Количество деревьев обновлено для пользователя {user_id}.")

    # Добавляем опыт (например, 10 XP за каждое дерево)
    xp_increment = 10
    async with conn.execute("""
        UPDATE users
        SET xp = xp + ?
        WHERE user_id = ?
    """, (xp_increment, user_id)):
        await conn.commit()
        print(f"[DEBUG] {xp_increment} XP добавлено пользователю {user_id}.")

    await conn.close()

# Функция для обновления прогресса миссии
async def update_mission_progress(user_id, mission_id, progress_increment):
    conn = await connect_db()
    async with conn.execute("""
        UPDATE user_missions
        SET progress = progress + ?
        WHERE user_id = ? AND mission_id = ?
    """, (progress_increment, user_id, mission_id)):
        await conn.commit()
    await conn.close()
    print(f"Mission {mission_id} progress updated for user {user_id}.")  # Отладочное сообщение

async def track_referral(user_id, referrer_id):
    conn = await connect_db()

    # Проверяем, существует ли уже запись о реферале для конкретного пользователя
    async with conn.execute("""
        SELECT * FROM referrals WHERE user_id = ? OR (user_id = ? AND referrer_id = ?)
    """, (user_id, referrer_id, user_id)) as cursor:
        referral = await cursor.fetchone()

    # Логируем, что нашлось в базе
    print(f"[DEBUG] Результат проверки реферала для пользователя {user_id}: {referral}")

    # Проверка 1: Если пользователь уже добавлен как чей-то реферал или добавлял данного пользователя
    if referral:
        print(f"[DEBUG] Пользователь {user_id} уже зарегистрирован как реферал, повторная запись запрещена.")
        return  # Выходим из функции, если реферал уже существует

    # Проверка 2: Запрет на взаимные рефералы
    async with conn.execute("""
        SELECT * FROM referrals WHERE user_id = ? AND referrer_id = ?
    """, (referrer_id, user_id)) as cursor:
        reverse_referral = await cursor.fetchone()

    if reverse_referral:
        print(f"[DEBUG] Взаимное добавление рефералов запрещено: {user_id} и {referrer_id}")
        return  # Запрещаем обоюдные рефералы

    # Если проверки пройдены, добавляем нового реферала
    async with conn.execute("""
        INSERT INTO referrals (user_id, referrer_id, timestamp)
        VALUES (?, ?, datetime('now'))
    """, (referrer_id, user_id)):
        await conn.commit()
        print(f"[DEBUG] Пользователь {user_id} добавлен как реферал к {referrer_id}.")

    # Обновляем количество рефералов у пригласившего пользователя
    async with conn.execute("""
        UPDATE users
        SET referrals = referrals + 1
        WHERE user_id = ?
    """, (referrer_id,)):
        await conn.commit()
        print(f"[DEBUG] Обновлено количество рефералов для пользователя {referrer_id}.")

    await conn.close()
    
    # Обновляем количество рефералов у пригласившего пользователя
    async with conn.execute("""
        UPDATE users
        SET referrals = referrals + 1
        WHERE user_id = ?
    """, (referrer_id,)):
        await conn.commit()
        print(f"[DEBUG] Обновлено количество рефералов для пользователя {referrer_id}.")
    
    await conn.close()