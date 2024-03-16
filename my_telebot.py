import os
import telebot
from dotenv import load_dotenv
from telebot import types

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Создаем клавиатуру главного меню
main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_menu_markup.row(types.KeyboardButton("Ссылка на сайт"), types.KeyboardButton("Наши Контакты"))
main_menu_markup.row(types.KeyboardButton("Прайс услуг"), types.KeyboardButton("Адрес офисов"),
                     types.KeyboardButton("Апостиль-Консульская легализация"))


def read_countries_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


# Функция для отправки главного меню
def send_main_menu(message):
    bot.send_message(message.chat.id, "Выберите действие из меню.", reply_markup=main_menu_markup)


# Функция для чтения списка стран из файла
def read_countries_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


# Обработчик команды /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = "Добро пожаловать в бюро переводов [Translit].\n\n" \
                      "Вы можете посетить наш веб-сайт, нажав кнопку 'Ссылка на сайт'."
    bot.reply_to(message, welcome_message, reply_markup=main_menu_markup)
    send_main_menu(message)


# Обработчик кнопки "Апостиль"
@bot.message_handler(func=lambda message: message.text == "Апостиль-Консульская легализация")
def send_apostille_info(message):
    apostille_info = "Апостиль - это международное удостоверение подлинности документов, " \
                     "применяемое в странах, участниках Гаагской конвенции 1961 года. " \
                     "Он упрощает процедуру признания документов за границей. " \
                     "Апостиль проставляется на документах официальными органами государства, " \
                     "выдавшего документ, и подтверждает подлинность подписи, качество печати и т. д."
    bot.reply_to(message, apostille_info)
    send_main_menu(message)
    send_countries_list(message)


@bot.message_handler(func=lambda message: message.text == "Список стран")
def send_countries_list(message):
    countries_list = read_countries_list("countries_list.txt")
    bot.reply_to(message, countries_list)
    send_main_menu(message)

    @bot.message_handler(func=lambda message: message.text == "Список стран")
    def send_countries_list(message):
        countries_list = read_countries_list("countries_list.txt")
        bot.reply_to(message, countries_list)
        send_main_menu(message)
    # Обработчик кнопок


@bot.message_handler(func=lambda message: message.text == "Ссылка на сайт")
def send_website_link(message):
    website_url = 'http://www.translit-nvrsk.ru'
    bot.reply_to(message, f"Вы можете посетить наш веб-сайт здесь: {website_url}")
    send_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Прайс услуг")
def send_price_list(message):
    price_list_url = 'http://www.translit-nvrsk.ru/ru/ct-menu-item-3'
    bot.reply_to(message, f"Вы можете посмотреть наш прайс услуг по ссылке: {price_list_url}")
    send_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Адрес офисов")
def send_office_address(message):
    office_address = 'г. Новороссийск, ул. Советов, 42 (БЦ "Черноморский"), офис №1,. г. Новороссийск, ул. Мира, 37 (рядом с нотариальной конторой)'
    bot.reply_to(message, f"Адрес наших офисов: {office_address}")
    send_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Наши Контакты")
def send_contacts(message):
    bot.send_message(message.chat.id, "Контакты офиса на улице Советов (офис №1):\n+79881313424",
                     reply_markup=main_menu_markup
