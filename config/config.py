# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

# Получаем токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Получаем ID администратора
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

if not TOKEN:
    raise ValueError("Токен не найден! Проверьте файл .env")

if not ADMIN_USER_ID:
    raise ValueError("ID администратора не найден! Проверьте файл .env")
