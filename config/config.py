# config/config.py
# Создайте файл config/config.py, в котором будет загружаться токен из .env:
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

# Получаем токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Проверьте файл .env")
