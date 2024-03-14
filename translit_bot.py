import os

import telebot
from dotenv import load_dotenv
from telebot import types

# Загрузка переменных окружения из файла .env
load_dotenv('. evn')

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# URL веб-сайта, ссылка на прайс-лист и адрес офисов
website_url = 'http://www.translit-nvrsk.ru'
price_list_url = 'http://www.translit-nvrsk.ru/ru/ct-menu-item-3'
office_address = 'г. Новороссийск, ул. Советов, 42 (БЦ "Черноморский"), офис №1,. г. Новороссийск, ул. Мира, 37 (рядом с нотариальной конторой)'

# Создаем клавиатуру главного меню
main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_menu_markup.row(types.KeyboardButton("Ссылка на сайт"), types.KeyboardButton("Наши Контакты"))
main_menu_markup.row(types.KeyboardButton("Прайс услуг"), types.KeyboardButton("Адрес офисов"),
                     types.KeyboardButton("Стоимость паспортов"), types.KeyboardButton("Апостил-Консульская легализация" ))


# Обработчик команды /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = "Добро пожаловать в бюро переводов [Translit].\n\n" \
                      "Вы можете посетить наш веб-сайт, нажав кнопку 'Ссылка на сайт'."
    bot.reply_to(message, welcome_message, reply_markup=main_menu_markup)
    send_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Стоимость паспортов")
def send_passport_price(message):
    passport_price_text = """Стоимость паспортов:
    - Перевод паспартов - 1200 руб.
    - Перевод с бередянского"""
    bot.reply_to(message, passport_price_text)
    send_main_menu(message)


# Обработчик кнопок
@bot.message_handler(func=lambda message:message.text == "Апостил-Консульская легализация")
def send_legalization_info(message):
    legalization_info = "Консульская легализация - это один из способов легализации документов при внешнеэкономической деятельности. " \
                        "Аналогичен апостилю. В отличие от апостиля применяется при документообороте с организациями, происходящими из стран, " \
                        "не являющихся участницами Гаагской конвенции об отмене требований легализации иностранных официальных документов. " \
                        "По сравнению с апостилем, является более сложной двусторонней процедурой."
    bot.reply_to(message, legalization_info)

#текстовый фаил с странами список
    with open('legalization_document.txt', 'rb') as document_file:
        bot.send_document(message.chat.id, document_file)

#фото пример доков
    with open('example_document.jpg', 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file)
    send_main_menu(message)



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
    office_address_1 = "Адрес офиса на улице Советов (офис №1):\nг. Новороссийск, ул. Советов, 42 (БЦ 'Черноморский')"
    office_address_2 = "Адрес офиса на улице Мира:\nг. Новороссийск, ул. Мира, 37 (рядом с нотариальной конторой)"

    bot.send_message(message.chat.id, office_address_1)
    bot.send_message(message.chat.id, office_address_2)
    send_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Наши Контакты")
def send_contacts(message):
    bot.send_message(message.chat.id, "Контакты офиса на улице Советов 42 (офис №1):\n+79628555915",
                     reply_markup=main_menu_markup)
    bot.send_message(message.chat.id, "Контакты офиса на улице Мира 37 (рядом с нотариальной конторой):\n+79883232525",
                     reply_markup=main_menu_markup)


# Функция для отправки главного меню
def send_main_menu(message):
    bot.send_message(message.chat.id, "Выберите действие из меню.", reply_markup=main_menu_markup)


# Главный цикл обработки сообщений

bot.polling(none_stop=True)
