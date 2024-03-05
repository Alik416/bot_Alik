import telebot
from telebot import types
from googletrans import Translator

# Используем ваш токен
bot = telebot.TeleBot('6321476948:AAFzW-mEe2LTCIai7zk_Ad2DipuFWxCtftU')

website_url = 'http://www.translit-nvrsk.ru/ru/'
phone_number = '+79881313424'
translator = Translator()

# Создаем клавиатуру
main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_menu_markup.row(types.KeyboardButton("Звонок на номер"), types.KeyboardButton("Ссылка на сайт"))
main_menu_markup.row(types.KeyboardButton("Список функций бота"), types.KeyboardButton("Отзыв и вопросы"))
main_menu_markup.row(types.KeyboardButton("Перевести с английского"))

# Обработчик команды /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = "Добро пожаловать в наше бюро переводов!\n\n" \
                      "Вы можете посетить наш веб-сайт, нажав кнопку 'Ссылка на сайт'."
    bot.reply_to(message, welcome_message, reply_markup=main_menu_markup)

# Обработчик кнопки "Ссылка на сайт"
@bot.message_handler(func=lambda message: message.text == "Ссылка на сайт")
def send_website_link(message):
    bot.reply_to(message, f"Вы можете посетить наш веб-сайт здесь: {website_url}")

# Обработчик кнопки "Звонок на номер"
@bot.message_handler(func=lambda message: message.text == "Звонок на номер")
def make_phone_call(message):
    bot.send_contact(message.chat.id, phone_number)

# Обработчик кнопки "Список функций бота"
@bot.message_handler(func=lambda message: message.text == "Список функций бота")
def send_function_list(message):
    function_list = "Список доступных функций:\n1. Функция 1\n2. Функция 2\n3. Функция 3"
    bot.send_message(message.chat.id, function_list)

# Обработчик кнопки "Отзыв и вопросы"
@bot.message_handler(func=lambda message: message.text == "Отзыв и вопросы")
def handle_feedback(message):
    response = "Спасибо за ваш отзыв или вопрос. Мы постараемся ответить как можно скорее."
    bot.send_message(message.chat.id, response)

# Обработчик кнопки "Перевести с английского"
@bot.message_handler(func=lambda message: message.text == "Перевести с английского")
def request_translation(message):
    bot.reply_to(message, "Введите текст для перевода с английского на русский.")
    bot.register_next_step_handler(message, process_translation)

def process_translation(message):
    try:
        text = message.text
        translated = translator.translate(text, src='en', dest='ru')
        bot.reply_to(message, f"Перевод: {translated.text}")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при переводе.")

# Запускаем бота
bot.polling(none_stop=True, interval=0)
