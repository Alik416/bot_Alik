import telebot
from telebot import types
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# URL веб-сайта, номер телефона, ссылка на прайс-лист и адрес офисов
website_url = 'http://www.translit-nvrsk.ru/ru'
phone_number = '+79883232525'
price_list_url = 'https://www.translit-nvrsk.ru/price_list'
office_address = 'г. Новороссийск, ул. Советов, 42 (БЦ "Черноморский"), офис №1,. г. Новороссийск, ул. Мира, 37 (рядом с нотариальной конторой)'

# Создаем клавиатуру главного меню
main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_menu_markup.row(types.KeyboardButton("Ссылка на сайт"), types.KeyboardButton("Звонок на номер"))
main_menu_markup.row(types.KeyboardButton("Прайс услуг"), types.KeyboardButton("Адрес офисов"))

# Обработчик команды /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = "Добро пожаловать в бюро переводов [Translit].\n\n" \
                      "Вы можете посетить наш веб-сайт, нажав кнопку 'Ссылка на сайт'."
    bot.reply_to(message, welcome_message, reply_markup=main_menu_markup)
    send_main_menu(message)

# Обработчик кнопок
@bot.message_handler(func=lambda message: message.text == "Ссылка на сайт")
def send_website_link(message):
    bot.reply_to(message, f"Вы можете посетить наш веб-сайт здесь: {website_url}")
    send_main_menu(message)

@bot.message_handler(func=lambda message: message.text == "Прайс услуг")
def send_price_list(message):
    bot.reply_to(message, f"Вы можете посмотреть наш прайс услуг по ссылке: {price_list_url}")
    send_main_menu(message)

@bot.message_handler(func=lambda message: message.text == "Адрес офисов")
def send_office_address(message):
    bot.reply_to(message, f"Адрес наших офисов: {office_address}")
    send_main_menu(message)

@bot.message_handler(func=lambda message: message.text == "Звонок на номер")
def make_phone_call(message):
    bot.send_contact(message.chat.id, phone_number)
    send_main_menu(message)

# Функция для отправки главного меню
def send_main_menu(message):
    bot.send_message(message.chat.id, "Выберите действие из меню.", reply_markup=main_menu_markup)

# Главный цикл обработки сообщений
bot.polling(none_stop=True)
