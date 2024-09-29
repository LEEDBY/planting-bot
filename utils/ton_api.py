# utils/ton_api.py

import requests
from config import TON_WALLET_ADDRESS, TON_API_KEY
import base64

# Функция для получения списка транзакций с кошелька через TON Center API
async def get_transactions(wallet_address):
    url = f"https://toncenter.com/api/v2/getTransactions"
    headers = {
        'Authorization': f'Bearer {TON_API_KEY}',
        'accept': 'application/json'
    }

    params = {
        'address': wallet_address,
        'limit': 10,
        'archival': 'true'  # Включаем архивные данные, если требуется
    }

    try:
        # Дебаг: перед отправкой запроса
        print(f"[DEBUG] Отправка запроса для получения транзакций с кошелька: {wallet_address}")

        # Отправляем GET-запрос к TON Center API
        response = requests.get(url, headers=headers, params=params)
        print(f"[DEBUG] Статус ответа API: {response.status_code}")
        
        response.raise_for_status()  # Если статус не 200, бросаем исключение
        data = response.json()

        # Дебаг: выводим полученные транзакции
        print(f"[DEBUG] Полученные транзакции: {data.get('result', [])}")
        
        return data.get('result', [])
    except requests.exceptions.HTTPError as http_err:
        print(f"[DEBUG] HTTP ошибка: {http_err}")
    except Exception as e:
        print(f"[DEBUG] Ошибка при получении транзакций: {e}")
    return []

# Функция для проверки платежа по MEMO
async def check_payment(memo):
    print(f"[DEBUG] Начало проверки платежа с MEMO: {memo}")

    transactions = await get_transactions(TON_WALLET_ADDRESS)

    # Проход по транзакциям для поиска платежа с нужным memo
    for transaction in transactions:
        print(f"[DEBUG] Проверка транзакции: {transaction}")
        
        # Извлекаем закодированный memo (Base64) из 'msg_data' → 'text'
        msg_data = transaction.get('in_msg', {}).get('msg_data', {})
        if msg_data.get('@type') == 'msg.dataText' and 'text' in msg_data:
            encoded_memo = msg_data['text']
            decoded_memo = base64.b64decode(encoded_memo).decode('utf-8')  # Декодируем Base64
            
            # Проверяем совпадение с переданным memo
            if decoded_memo == memo:
                print(f"[DEBUG] Платеж найден с MEMO: {memo}, сумма: {transaction['in_msg']['value']}")
                return {
                    'amount': transaction['in_msg']['value'],  # Сумма транзакции
                    'timestamp': transaction['utime']  # Время транзакции
                }

    print(f"[DEBUG] Платеж с MEMO: {memo} не найден.")
    return None