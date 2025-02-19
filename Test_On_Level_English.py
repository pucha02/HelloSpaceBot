import telebot
from telebot import types



def send_next_question(chat_id, user_data, bot, calculate_level):
    user = user_data.get(chat_id)
    if user is None:
        return

    questions = user["questions"]
    current_question = user["current_question"]

    if current_question < len(questions):
        question_data = questions[current_question]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        
        # Добавляем опции для вопроса
        for option in question_data["options"]:
            markup.add(types.KeyboardButton(option))
        
        # Добавляем кнопку "Выйти"
        markup.add(types.KeyboardButton("Завершити тест"))
        
        bot.send_message(chat_id, question_data["question"], reply_markup=markup)
    else:
        calculate_level(chat_id, user_data, bot)


def send_welcome(chat_id, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton('Грамматика')
    item2 = types.KeyboardButton('Лексика')
    item3 = types.KeyboardButton('🏠 Головне меню')
    markup.add(item1, item2)
    markup.add(item3)
    
    bot.send_message(chat_id, "Оберіть тест 👇", reply_markup=markup)
# Рассчет уровня после завершения теста
def calculate_level(chat_id, user_data, bot):
    user = user_data.get(chat_id)
    if user is None:
        return
    
    score = user["score"]
    total_questions = len(user["questions"])

    # Определяем уровень по количеству правильных ответов
    if score <= total_questions * 0.2:
        level = "A1"
    elif score <= total_questions * 0.4:
        level = "A2"
    elif score <= total_questions * 0.6:
        level = "B1"
    elif score <= total_questions * 0.8:
        level = "B2"
    elif score <= total_questions * 0.9:
        level = "C1"
    else:
        level = "C2"

    bot.send_message(chat_id, f"Твій рівень: {level}. Ти відповів правильно на {score} з {total_questions} питань.")
    send_welcome(chat_id, bot)
    

