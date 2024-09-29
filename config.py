# config.py

import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Поддерживаемые языки
SUPPORTED_LANGUAGES = ['en', 'ru', 'es']
DEFAULT_LANGUAGE = 'en'

# Путь к директории с файлами локализации
LOCALES_DIR = os.path.join(os.path.dirname(__file__), 'locales')

# Адрес вашего кошелька TON
TON_WALLET_ADDRESS = "UQC8zbNhEeh4EuRtHVL4GvGIC63RW3SNmYWz-6AtUFbXEgCH"
TON_API_URL = 'https://tonapi.io'  # URL API для работы с блокчейном TON
TON_API_KEY = 'adb31b12d074c54befe2f187c2dbdb1bd273338d1aededd077681f18d170ce97'  # API-ключ для доступа к TON API

# Минимальная сумма для посадки дерева (TON)
MIN_DONATION_AMOUNT = 0.1  # 10 TON

# Время действия чека (в минутах)
CHECK_EXPIRATION_TIME = 10  # Чек действителен 10 минут

# Интервал проверки платежей (в секундах)
PAYMENT_CHECK_INTERVAL = 20  # Проверка раз в 60 секунд

# Сумма пожертвования (если фиксированная)
DONATION_AMOUNT = 0.1  # 10 TON
