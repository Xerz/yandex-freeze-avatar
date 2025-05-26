import requests
import os
import logging  # Добавляем импорт logging
from dotenv import load_dotenv
load_dotenv()

YANDEX_API_TOKEN = os.environ.get("YANDEX_API_TOKEN")
YANDEX_API_URL = "https://login.yandex.ru/info"
headers = {"Authorization": f"OAuth {YANDEX_API_TOKEN}"}

def get_avatar_id():
    try:
        response = requests.get(YANDEX_API_URL, headers=headers, timeout=10)
        response.raise_for_status()  # Проверяем статус ответа
        return response.json()["default_avatar_id"]
    except requests.exceptions.RequestException as e:
        # Логируем ошибку и пробрасываем исключение
        logging.error(f"Failed to fetch avatar ID: {e}", exc_info=True)
        raise
