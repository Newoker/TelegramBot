# bot/bot.py
# Создайте файл bot/bot.py, который будет содержать логику инициализации бота
from telegram import Bot
from config.config import TOKEN

def create_bot():
    """Создаем и возвращаем объект бота"""
    bot = Bot(token=TOKEN)
    return bot
