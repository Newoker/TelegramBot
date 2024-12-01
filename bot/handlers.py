from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
import re
from config.config import ADMIN_USER_ID

# Состояния для обработки ввода формы
FORM_STATE = "form_state"

# Список для хранения добавленных пользователей (можно заменить на базу данных)
user_list = []  # Список в формате: [{'username': 'ник', 'dob': 'день.месяц.год'}]

async def start(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    keyboard = [
        ["🚀 Старт", "❓ Помощь"],  # Используем эмодзи для кнопок
        ["👨‍💻 Админ"]  # Эмодзи для кнопки "Админ"
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Привет! Я твой Telegram-бот! Выберите действие:",
        reply_markup=reply_markup
    )

async def help(update: Update, context: CallbackContext):
    """Обработчик команды /help"""
    await update.message.reply_text("Как я могу помочь? Напишите мне, если что-то нужно!")

async def admin(update: Update, context: CallbackContext):
    """Обработчик команды /admin, доступной только администратору"""
    if update.message.from_user.id == int(ADMIN_USER_ID):
        keyboard = [["Добавить", "Список", "Назад"]]  # Кнопка "Назад" для возврата в главное меню
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Привет, администратор! Выберите действие:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("У вас нет прав для выполнения этой команды. 🚫")

async def add(update: Update, context: CallbackContext):
    """Обработчик кнопки "Добавить"""
    if update.message.from_user.id == int(ADMIN_USER_ID):
        await update.message.reply_text(
            "Заполните форму в следующем виде:\n1. Имя (Телеграм ID, например @vien)\n2. День рождения (в формате ДЕНЬ.МЕСЯЦ.ГОД)",
            reply_markup=ReplyKeyboardMarkup([["❌ Отмена", "Назад"]], resize_keyboard=True)
        )
        # Устанавливаем состояние, чтобы ждать ввод формы
        context.user_data[FORM_STATE] = True
    else:
        await update.message.reply_text("Эта команда доступна только для администратора.")


async def handle_form_input(update: Update, context: CallbackContext):
    """Обработчик ввода данных для формы"""
    
    # Проверка на нажатие кнопки "❌ Отмена"
    if update.message.text == "❌ Отмена":
        # Отправляем сообщение об отмене добавления
        await update.message.reply_text(
            "Отмена добавления.",
            reply_markup=ReplyKeyboardMarkup([["Добавить", "Список", "Назад"]], resize_keyboard=True)
        )
        del context.user_data[FORM_STATE]  # Очистка состояния
        return

    # Обработка формы, если состояние формы активно
    if FORM_STATE in context.user_data:
        # Получаем текст, который прислал пользователь
        user_input = update.message.text
        # Проверяем, что текст соответствует формату @ник и день.месяц.год
        match = re.match(r"^@(\w+)\s(\d{2})\.(\d{2})\.(\d{4})$", user_input)

        if match:
            username, day, month, year = match.groups()

            # Проверка, если такой пользователь уже есть в списке
            if any(user['username'] == username for user in user_list):
                # Отправляем сообщение, если человек уже в списке
                await update.message.reply_text(
                    "Такой человек уже находится в списке.",
                    reply_markup=ReplyKeyboardMarkup([["❌ Отмена", "Список", "Назад"]], resize_keyboard=True)
                )
                return

            # Добавляем нового пользователя в список
            user_list.append({'username': username, 'dob': f"{day}.{month}.{year}"})
            
            # Подтверждение добавления
            await update.message.reply_text(
                f"Спасибо! Вы добавили:\nИмя: @{username}\nДата рождения: {day}.{month}.{year}",
                reply_markup=ReplyKeyboardMarkup([["❌ Отмена", "Список", "Назад"]], resize_keyboard=True)
            )
            
            # После успешного ввода сбрасываем состояние формы
            del context.user_data[FORM_STATE]

        else:
            await update.message.reply_text(
                "Неправильная форма. Пожалуйста, заполните форму заново в правильном формате:\n@ник\nДЕНЬ.МЕСЯЦ.ГОД",
                reply_markup=ReplyKeyboardMarkup([["❌ Отмена", "Список", "Назад"]], resize_keyboard=True)
            )

    elif update.message.text == "Назад":
        # Возвращаем пользователя в основное меню
        await start(update, context)  # Отправляем команду /start
        del context.user_data[FORM_STATE]  # Очистка состояния формы, чтобы не возвращаться к ней

    elif update.message.text == "Список":
        # Отправляем список всех добавленных пользователей
        if user_list:
            user_list_text = "\n".join([f"@{user['username']} - {user['dob']}" for user in user_list])
            await update.message.reply_text(
                f"Список добавленных пользователей:\n{user_list_text}",
                reply_markup=ReplyKeyboardMarkup([["Добавить", "Список", "Назад"]], resize_keyboard=True)
            )
        else:
            await update.message.reply_text(
                "Список пуст. Еще нет добавленных пользователей.",
                reply_markup=ReplyKeyboardMarkup([["Добавить", "Список", "Назад"]], resize_keyboard=True)
            )

    elif update.message.text == "Добавить":
        # Включаем состояние формы для добавления пользователя
        context.user_data[FORM_STATE] = True
        await update.message.reply_text(
            "Введите данные в формате:\n@ник\nДЕНЬ.МЕСЯЦ.ГОД",
            reply_markup=ReplyKeyboardMarkup([["❌ Отмена", "Список", "Назад"]], resize_keyboard=True)
        )