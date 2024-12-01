import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Получаем токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Проверьте файл .env")

print(f"Ваш токен: {TOKEN}")
