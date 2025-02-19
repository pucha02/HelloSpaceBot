from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import telebot



def teachers_menu(message, bot, update_last_interaction, teachers_data):
    chat_id = message.chat.id
    markups = ReplyKeyboardMarkup(resize_keyboard=True)

    # Переменная для хранения списка кнопок
    buttons = []
    
    # Создаем кнопки для каждого учителя и добавляем их в список
    for teacher_name in teachers_data.keys():
        button = KeyboardButton(teacher_name)
        buttons.append(button)

    # Размещаем кнопки по 2 в ряд
    for i in range(0, len(buttons), 3):
        markups.row(*buttons[i:i+3])

    # Кнопка для возврата в главное меню
    button_main_menu = KeyboardButton("🏠 Головне меню")
    markups.add(button_main_menu)

    bot.send_message(chat_id, "🌟 Наші викладачі готові допомогти вам досягти ваших мовних цілей. Кожен з них має свій унікальний стиль навчання.", reply_markup=markups)
    bot.send_message(chat_id, "Обирайте викладача 👇")
 
    update_last_interaction(message)


# Функция для обработки нажатий на кнопки с именами учителей
def handle_teacher_choice(message, bot, teachers_data):
    chat_id = message.chat.id
    teacher_name = message.text  # Получаем текст нажатой кнопки (имя учителя)

    if teacher_name in teachers_data:
        # Получаем информацию и фото о выбранном учителе
        teacher_info = teachers_data[teacher_name]["text"]
        teacher_photo = teachers_data[teacher_name]["photo"]

        # Отправляем фото и информацию о выбранном учителе
        bot.send_photo(chat_id, teacher_photo, caption=teacher_info, parse_mode='Markdown')
    else:
        # Если имя не найдено, отправляем сообщение об ошибке
        bot.send_message(chat_id, "Вибачте, такого викладача немає в списку.")
