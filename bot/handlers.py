# bot/handlers.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from config.config import ADMIN_USER_ID  # Импортируем ID админа


async def start(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    await update.message.reply_text("Привет! Я твой Telegram-бот!")

async def help(update: Update, context: CallbackContext):
    """Обработчик команды /help"""
    await update.message.reply_text("Как я могу помочь?")


async def admin(update: Update, context: CallbackContext):
    """Обработчик команды /admin, доступной только администратору"""
    # Проверяем, является ли пользователь администратором
    if update.message.from_user.id == int(ADMIN_USER_ID):
        await update.message.reply_text("Привет, администратор! Чем могу помочь?")
    else:
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")
