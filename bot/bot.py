from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config.config import TOKEN  # Токен для бота
from bot.handlers import start, help, admin, add, handle_form_input, delete, check_birthdays  # Импортируем обработчики
from telegram import Update
import datetime
import schedule
import time


# Пример обработки команды для получения chat_id
async def get_chat_id(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")

def job():
    """Функция для проверки первого дня месяца"""
    now = datetime.datetime.now()
    if now.day == 1:  # Проверка первого дня месяца
        send_birthday_reminders(None)  # Передаем None вместо update, так как в этой функции оно не используется

async def button_handler(update: Update, context: CallbackContext):
    """Обработчик нажатия кнопок, которые отправляют команды"""
    text = update.message.text

    if text == "🚀 Старт":
        await start(update, context)  # Отправляем команду /start
    elif text == "❓ Помощь":
        await help(update, context)  # Отправляем команду /help
    elif text == "👨‍💻 Админ":
        await admin(update, context)  # Отправляем команду /admin
    elif text == "Добавить":
        await add(update, context)  # Отправляем команду для добавления дня рождения
    elif text == "Удалить":
        # Обрабатываем запрос на удаление
        await delete(update, context)  # Устанавливаем состояние удаления
    else:
        await handle_form_input(update, context)  # Обрабатываем форму, если она активна

async def send_birthday_reminders(context: CallbackContext):
    """Запускаем проверку дней рождения"""
    # Получаем чат ID, куда отправлять сообщения (например, ID админ-канала)
    chat_id = -1001790737635  # Укажите здесь ID чата
    
    # Отправляем сообщение без создания объекта update
    await context.bot.send_message(chat_id=chat_id, text="Проверка дней рождения...")
    
    # Здесь проверка и отправка напоминаний о днях рождения
    await check_birthdays(chat_id, context)  # Передаем chat_id для отправки сообщений

async def check_birthday_command(update: Update, context: CallbackContext):
    """Запуск проверки дней рождения через команду"""
    await send_birthday_reminders(context)

def main() -> None:
    """Основная функция для запуска бота."""
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CommandHandler("chatid", get_chat_id))
    application.add_handler(CommandHandler("check_birthday", check_birthday_command))

    # Регистрируем обработчик нажатия кнопок
    application.add_handler(MessageHandler(filters.TEXT, button_handler))

    # Запускаем планировщик задач, который будет выполняться каждый день
    schedule.every().day.at("09:00").do(job)

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
