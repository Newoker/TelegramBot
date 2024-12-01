# bot/bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config.config import TOKEN  # Токен для бота
from bot.handlers import start, help, admin  # Исправленный импорт обработчиков

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я твой Telegram-бот!")

# Основная функция для запуска бота
def main() -> None:
    """Основная функция для запуска бота."""
    # Создаем приложение (бота) с токеном
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("admin", admin))  # Регистрация команды /admin

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()