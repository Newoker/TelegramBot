import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Загружаем переменные из .env
load_dotenv()

# Получаем токен из переменных окружения
token = os.getenv("TELEGRAM_BOT_TOKEN")

if not token:
    raise ValueError("Токен не найден! Проверьте файл .env")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я ваш Telegram бот.")

# Основная функция для запуска бота
def main() -> None:
    # Создаем приложение (бота) с токеном
    application = Application.builder().token(token).build()

    # Регистрируем обработчик для команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
