from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config.config import TOKEN  # Токен для бота
from bot.handlers import start, help, admin  # Импортируем обработчики из handlers.py
from telegram import Update, ReplyKeyboardMarkup

async def button_handler(update: Update, context: CallbackContext):
    """Обработчик нажатия кнопок, которые отправляют команды"""
    text = update.message.text

    if text == "Старт":
        await start(update, context)  # Отправляем команду /start
    elif text == "Помощь":
        await help(update, context)  # Отправляем команду /help
    elif text == "Админ":
        await admin(update, context)  # Отправляем команду /admin

def main() -> None:
    """Основная функция для запуска бота."""
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("admin", admin))

    # Регистрируем обработчик нажатия кнопок
    application.add_handler(MessageHandler(filters.TEXT, button_handler))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
