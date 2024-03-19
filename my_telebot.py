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
website_url = "http://www.translit-nvrsk.ru"
photo_urls = [
    "https://drive.google.com/uc?id=1wqPNOx7ajvyhZDtz7L-49jmp7LEenZDR",  # Фото 1
    "https://drive.google.com/uc?id=1g1uNDV5N7DUdCKADRGEnGVT_uiloTcrj",  # Фото 2
    "https://drive.google.com/uc?id=1NJ-YlqxRT91auAzrjduEZdwYxUZhJjcv"  # Фото 3
]
captions = ["Пример документа 1",
            "Пример документа 2",
            "Пример документа 3"
            ]

# Создаем клавиатуру главного меню
main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_menu_markup.row(types.KeyboardButton("Ссылка на сайт"), types.KeyboardButton("Наши Контакты"))
main_menu_markup.row(types.KeyboardButton("Прайс услуг"), types.KeyboardButton("Апостиль-Консульская легализация"))


@bot.message_handler(func=lambda message: message.text == "Прайс услуг")
def send_price_list(message):
    price_list_url = "http://www.translit-nvrsk.ru/ru/ct-menu-item-3"
    bot.reply_to(message, f"Вы можете посмотреть наш прайс услуг по ссылке: {price_list_url}")
    send_main_menu(message)


# Функция для чтения списка стран из файла
def read_countries_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()  # Прочитать строки как список


# Функция для отправки главного меню
def send_main_menu(message):
    bot.send_message(message.chat.id, "Выберите действие из меню.", reply_markup=main_menu_markup)


# Обработчик команды /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = "Добро пожаловать в бюро переводов [Translit].\n\n" \
                      "Вы можете посетить наш веб-сайт, нажав кнопку 'Ссылка на сайт'."
    bot.reply_to(message, welcome_message, reply_markup=main_menu_markup)
    send_main_menu(message)


# Обработчик кнопки "Апостиль"
@bot.message_handler(func=lambda message: message.text.strip().lower() == "Апостиль-Консульская легализация")
def send_apostille_info(message):
    apostille_info = "Апостиль - это международное удостоверение подлинности документов, применяемое в странах, участниках Гаагской конвенции 1961 года. Он упрощает процедуру признания документов за границей. Апостиль проставляется на документах официальными органами государства, выдавшего документ, и подтверждает подлинность подписи, качество печати и т. д."

    # Отправляем текстовую информацию
    bot.send_message(message.chat.id, apostille_info)

    # Создаем клавиатуру с тремя кнопками
    apostille_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    apostille_markup.row(types.KeyboardButton("Список стран"), types.KeyboardButton("Пример готового документа"),
                         types.KeyboardButton("Вернуться на главное меню"))

    # Отправляем клавиатуру
    bot.send_message(message.chat.id, "Что вас интересует?", reply_markup=apostille_markup)


@bot.message_handler(func=lambda message: message.text == "Список стран")
def send_countries_list(message):
    countries_list = read_countries_list("countries_list.txt")
    countries_text = "\n".join(countries_list)  # Собрать все строки в одну строку, разделяя их переводом строки
    bot.reply_to(message, countries_text)
    send_main_menu(message)


# Обработчик кнопки "Пример готового документа"
@bot.message_handler(func=lambda message: message.text == "Пример готового документа")
def send_example_document(message):
    for photo_url, caption in zip(photo_urls, captions):
        bot.send_photo(message.chat.id, photo_url, caption=caption)
    send_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Ссылка на сайт")
def send_website_link(message):
    bot.reply_to(message, f"Вы можете посетить наш веб-сайт здесь: {website_url}")
    send_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Наши Контакты")
def send_contacts(message):
    contacts = ("Контакты офиса на улице Советов 42 (офис №1):\n"
                "Телефон: +7 (988) 323-25-25\n"
                "Адрес: г. Новороссийск, ул. Советов, 42 (БЦ 'Черноморский'), офис №1\n\n"
                "Контакты офиса на улице Мира 37 (рядом с нотариальной конторой):\n"
                "Телефон: +7 (962) 855-59-15\n"
                "Адрес: г. Новороссийск, ул. Мира, 37 (рядом с нотариальной конторой)")
    bot.send_message(message.chat.id, contacts)
    send_main_menu(message)


@bot.message_handler(func=lambda message: message.text == "Геопозиция офиса на улице Советов, 42")
def send_office_location_sovetov(message):
    google_maps_url_sovetov = "https://maps.app.goo.gl/GRd67np5XfRJkgsJ9"
    bot.send_message(message.chat.id, "Ссылка на Google Maps для офиса на улице Советов, 42:", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Открыть Google Maps", url=google_maps_url_sovetov)))


# Обработчик кнопки "Вернуться на главное меню"
@bot.message_handler(func=lambda message: message.text == "Вернуться на главное меню")
def return_to_main_menu(message):
    send_main_menu(message)


# Главный цикл обработки сообщений
bot.polling(none_stop=True)
