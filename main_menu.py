from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def send_main_menu(message, admins, bot, update_last_interaction, message_id=None):
    chat_id = message.chat.id
    markup = InlineKeyboardMarkup()
    markups = ReplyKeyboardMarkup(resize_keyboard=True)
    button_contact = KeyboardButton("👨‍🏫 Хочу навчатись", request_contact=True)
    button_aboutUs = KeyboardButton("🏫 Про Школу")
    button_contacts = KeyboardButton("📍 Наші контакти")
    button_members_menu = KeyboardButton("👩‍🏫 Наші викладачі")
    button_training_menu = KeyboardButton("📊 Дізнатися свій рівень")
    button_learning_menu = KeyboardButton("📚 Про навчання")

# Создаем разметку с несколькими строками
    markups = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markups.add(button_aboutUs, button_learning_menu)  
    markups.add(button_training_menu)                  
    markups.add(button_members_menu)                   
    markups.add(button_contacts, button_contact)  

    markup.row_width = 1
    buttons = []
    if chat_id in admins:
        # buttons.append(InlineKeyboardButton("Ввести новину користувачу", callback_data="enter_news"))
        buttons.append(InlineKeyboardButton("Розіслати новину всім", callback_data="send_to_all"))
    markup.add(*buttons)
    
    bot.send_message(chat_id, "Обирайте кнопками, що цікавить👇", reply_markup=markups)
    
    if chat_id in admins:
        bot.send_message( chat_id,"🤗Я допоможу Вам вибрати потрібне:", reply_markup=markup)


    update_last_interaction(message)