def send_contacts(message):
    contacts = ("Контакты офиса на улице Советов (офис №1):\n"
                "Телефон: +7 (988) 323-25-25\n"
                "Адрес: г. Новороссийск, ул. Советов, 42 (БЦ 'Черноморский'), офис №1\n\n"
                "Контакты офиса на улице Мира (рядом с нотариальной конторой):\n"
                "Телефон: +7 (962) 855-59-15\n"
                "Адрес: г. Новороссийск, ул. Мира, 37 (рядом с нотариальной конторой)")
    bot.send_message(message.chat.id, contacts, reply_markup=contacts_markup)


@bot.message_handler(func=lambda message: message.text == "Геопозиция офиса на Советов, 42")
def send_office_location_sovetov(message):
    google_maps_url_sovetov = "https://maps.app.goo.gl/GRd67np5XfRJkgsJ9"
    bot.send_message(message.chat.id, "Ссылка на Google Maps для офиса на улице Советов, 42:", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Открыть Google Maps", url=google_maps_url_sovetov)))
