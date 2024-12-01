# telegram.py
from telegram.ext import Updater, CommandHandler
from bot.bot import create_bot
from bot.handlers import start, help

def main():
    """Главная функция для запуска бота"""
    # Создаем бота
    bot = create_bot()

    # Создаем Updater, который будет работать с ботом
    updater = Updater(bot=bot)

    # Регистрируем обработчики
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
