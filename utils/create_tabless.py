# utils/create_tables.py
from db import connect_db

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        language_code TEXT,
        trees_planted INTEGER DEFAULT 0,
        referrals INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 0
    );
    """)

    # Создание таблицы прогресса по миссиям
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_missions (
        user_id INTEGER,
        mission_id TEXT,
        progress INTEGER DEFAULT 0,
        status TEXT DEFAULT 'in_progress',
        PRIMARY KEY (user_id, mission_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    # Создание таблицы прогресса по достижениям
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_achievements (
        user_id INTEGER,
        achievement_id TEXT,
        progress INTEGER DEFAULT 0,
        status TEXT DEFAULT 'in_progress',
        PRIMARY KEY (user_id, achievement_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    conn.commit()
    conn.close()

# Таблица для хранения истории пожертвований
cursor.execute("""
CREATE TABLE IF NOT EXISTS donation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount DECIMAL(10, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""")

if __name__ == "__main__":
    create_tables()
