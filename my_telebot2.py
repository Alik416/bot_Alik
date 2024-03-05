import os
import sqlite3
from typing import Optional

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена бота из переменных окружения
bot_token: Optional[str] = os.getenv("BOT_TOKEN")
print("Значение переменной bot_token:", bot_token)

# Проверка наличия токена бота
if bot_token is None:
    raise ValueError("Токен бота не найден в переменных окружения.")

# Получение информации о пользователе по его идентификатору
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE user_id=?''', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Создаем подключение к базе данных и курсор
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Получаем информацию о существующем пользователе
user_id = 123456789
existing_user = get_user(user_id)

# Если пользователь не существует, добавляем его в базу данных
if existing_user is None:
    user_id = 123456789
    username = "user1"
    language = "en"
    theme = "dark"
    cursor.execute('''INSERT INTO users (user_id, username, language, theme)VALUES (?, ?, ?, ?)''',
                   (user_id, username, language, theme))
    conn.commit()

# Создаем таблицу пользователей, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  language TEXT,
                  theme TEXT
                  )''')

# Закрываем подключение к базе данных
conn.close()

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    existing_user = get_user(user_id)
    url = "https://www.translit-nvrsk.ru/"
    url_button = InlineKeyboardButton(text="Перейти на сайт", url=url)
    phone_button = InlineKeyboardButton(text="Звонок на номер", callback_data="+79883232525")
    price_button = InlineKeyboardButton(text="Прайс услуг", callback_data="price")


    reply_markup = InlineKeyboardMarkup([[url_button], [phone_button], [price_button]])
    update.message.reply_text("Нажмите на кнопку, чтобы перейти на сайт:", reply_markup=reply_markup)

# Добавление пользователя в базу данных
def add_user(user_id, username, language, theme):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (user_id, username, language, theme)
    VALUES (?, ?, ?, ?)''', (user_id, username, language, theme))
    conn.commit()
    conn.close()

# Обновление настроек пользователя
def update_preferences(user_id, language, theme):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE users SET language=?, theme=? WHERE user_id=?''', (language, theme, user_id))
    conn.commit()
    conn.close()

def main() -> None:
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

