from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from config.config import ADMIN_USER_ID

async def start(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    keyboard = [
        ["🚀 Старт", "❓ Помощь"],  # Используем эмодзи для кнопок
        ["👨‍💻 Админ"]  # Эмодзи для кнопки "Админ"
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Добавляем обработку нажатий
    await update.message.reply_text(
        "Привет! Я твой Telegram-бот! Выберите действие:",
        reply_markup=reply_markup
    )

async def help(update: Update, context: CallbackContext):
    """Обработчик команды /help"""
    # Реагируем на нажатие кнопки "Помощь" (отправляется команда /help)
    await update.message.reply_text("Как я могу помочь?")

async def admin(update: Update, context: CallbackContext):
    """Обработчик команды /admin, доступной только администратору"""
    # Реагируем на нажатие кнопки "Админ" (отправляется команда /admin)
    if update.message.from_user.id == int(ADMIN_USER_ID):
        await update.message.reply_text("Привет, администратор! Чем могу помочь?")
    else:
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")
