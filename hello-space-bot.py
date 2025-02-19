import base64
import json
import hashlib
import subprocess
import requests
import telebot
import time
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import threading
from pymongo import MongoClient
import schedule
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from test_level import start_quiz, send_question, calculate_result
from send_news import enter_news, send_news_to_user, send_news_to_all
from main_menu import send_main_menu
from about_school_menu import about_school_menu, why_we, popular_question
from learn_menu import learn_menu, course_structure, format_learn, course_deteil, show_price, show_about_course
from contacts import contacts
from Test_On_Level_English import send_next_question, calculate_level, send_welcome
from teachers_menu import teachers_menu, handle_teacher_choice

admins = [7293016451]  # ID администраторов
CONTACT_RECEIVER_CHAT_ID = 635258639

#7136284096:AAGjmsq4z_iPg9oWnEg4aqv3sv5qsAB_m0U - TEST API
#7486039291:AAHUoKYAHnBLQ49uVAAyQFNQTlbmKWNnHW4 - MAIN API

API_TOKEN = '7486039291:AAHUoKYAHnBLQ49uVAAyQFNQTlbmKWNnHW4'
client = MongoClient('mongodb+srv://hellospace2024:DFavIxnWstkWjkDS@cluster0.fnq8d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', 
                     tls=True, tlsAllowInvalidCertificates=True)

db = client['bot']
users_collection = db['users']

bot = telebot.TeleBot(API_TOKEN)
local_timezone = pytz.timezone('Europe/Kiev')

user_data = {}
user_answers = {}
user_scores = {}
last_interaction_times = {}
user_states = {}
user_contacts = {}
admin_news = {}
selected_users = {}

class States:
    WELCOME = "WELCOME"
    CHOOSING_OPTION = "CHOOSING_OPTION"
    CHOOSING_DIRECTION = "CHOOSING_DIRECTION"
    CHOOSING_MEMBERS = "CHOOSING_MEMBERS"
    CHOOSING_FORMAT = "CHOOSING_FORMAT"
    LEAVE_CONTACT = "LEAVE_CONTACT"
    PAYMENT = "PAYMENT"
    ENTERING_NEWS = "ENTERING_NEWS"
    CHOOSING_USER = "CHOOSING_USER"
    CONFIRM_SENDING_TO_USER = "CONFIRM_SENDING_TO_USER"
    CONFIRM_SENDING_TO_ALL = "CONFIRM_SENDING_TO_ALL"

# questions = [
#     {
#         'question': 'What is the past form of the verb "go"?',
#         'correct': 'went'
#     },
#     {
#         'question': 'Which one is a synonym for "happy"?',
#         'correct': 'joyful'
#     },
#     {
#         'question': 'Write the correct sentence: "I ___ a dog." (have/has)',
#         'correct': 'have'
#     },
# ]


grammar_questions = [
    {"level": "A1", "question": "1️⃣ з 1️⃣2️⃣\nShe ___ a student.", "options": ["is", "are", "am", "be"], "answer": "is"},
    {"level": "A1", "question": "2️⃣ з 1️⃣2️⃣\nI ___ coffee every morning.", "options": ["drink", "drinks", "drinking", "drank"], "answer": "drink"},
    # Добавьте еще 8 питань для A1
    {"level": "A2", "question": "3️⃣ з 1️⃣2️⃣\nWhere ___ you go yesterday?", "options": ["did", "does", "do", "are"], "answer": "did"},
    {"level": "A2", "question": "4️⃣ з 1️⃣2️⃣\nI haven’t seen him ___ a long time.", "options": ["since", "for", "by", "at"], "answer": "for"},
    # Добавьте еще 8 питань для A2
    {"level": "B1", "question": "5️⃣ з 1️⃣2️⃣\nIf I ___ more time, I would help you.", "options": ["have", "had", "would have", "will have"], "answer": "had"},
    {"level": "B1", "question": "6️⃣ з 1️⃣2️⃣\nThe film was ___ interesting than I expected.", "options": ["much", "more", "very", "many"], "answer": "more"},
    # Добавьте еще 8 питань для B1
    {"level": "B2", "question": "7️⃣ з 1️⃣2️⃣\nBy the time we arrived, they ___ dinner.", "options": ["had finished", "finished", "have finished", "are finishing"], "answer": "had finished"},
    {"level": "B2", "question": "8️⃣ з 1️⃣2️⃣\nShe told me that she ___ the book already.", "options": ["reads", "was reading", "had read", "is reading"], "answer": "had read"},
    # Добавьте еще 8 питань для B2
    {"level": "C1", "question": "9️⃣ з 1️⃣2️⃣\nI wish I ___ the truth earlier.", "options": ["know", "had known", "have known", "would know"], "answer": "had known"},
    {"level": "C1", "question": "🔟 з 1️⃣2️⃣\nThe project was delayed ___ a lack of funding.", "options": ["because", "due to", "despite", "since"], "answer": "due to"},
    # Добавьте еще 8 питань для C1
    {"level": "C2", "question": "1️⃣1️⃣ з 1️⃣2️⃣\nThe politician’s speech was filled with ___ rhetoric.", "options": ["persuasive", "incoherent", "verbose", "laconic"], "answer": "verbose"},
    {"level": "C2", "question": "1️⃣2️⃣ з 1️⃣2️⃣\nHis argument was both ___ and incisive.", "options": ["flawed", "compelling", "dull", "redundant"], "answer": "compelling"},
    # Добавьте еще 8 питань для C2
]

# Вопросы на лексику для всех уровней
vocabulary_questions = [
    {"level": "A1", "question": "1️⃣ з 1️⃣2️⃣\nWhat is the opposite of 'cold'?", "options": ["hot", "cool", "warm", "chilly"], "answer": "hot"},
    {"level": "A1", "question": "2️⃣ з 1️⃣2️⃣\nWhich word means the same as 'start'?", "options": ["begin", "finish", "stop", "continue"], "answer": "begin"},
    # Добавьте еще 8 питань для A1
    {"level": "A2", "question": "3️⃣ з 1️⃣2️⃣\nWhat is a synonym for 'job'?", "options": ["career", "salary", "profession", "task"], "answer": "career"},
    {"level": "A2", "question": "4️⃣ з 1️⃣2️⃣\nFill in the blank: He ___ his friends for a big party last weekend.", "options": ["invited", "brought", "met", "called"], "answer": "invited"},
    # Добавьте еще 8 питань для A2
    {"level": "B1", "question": "5️⃣ з 1️⃣2️⃣\nChoose the word that best fits the sentence: She is very ___ and always tells the truth.", "options": ["honest", "clever", "brave", "funny"], "answer": "honest"},
    {"level": "B1", "question": "6️⃣ з 1️⃣2️⃣\nHe refused to ___ the invitation.", "options": ["accept", "receive", "get", "take"], "answer": "accept"},
    # Добавьте еще 8 питань для B1
    {"level": "B2", "question": "7️⃣ з 1️⃣2️⃣\nWhat is the meaning of the idiom 'to beat around the bush'?", "options": ["to avoid talking about the main issue", "to go directly to the point", "to be aggressive", "to beat someone"], "answer": "to avoid talking about the main issue"},
    {"level": "B2", "question": "8️⃣ з 1️⃣2️⃣\nChoose the word closest in meaning to 'exhausted'.", "options": ["tired", "energetic", "bored", "relaxed"], "answer": "tired"},
    # Добавьте еще 8 питань для B2
    {"level": "C1", "question": "9️⃣ з 1️⃣2️⃣\nThe word 'ambivalent' means:", "options": ["having mixed feelings", "uncertain", "hostile", "friendly"], "answer": "having mixed feelings"},
    {"level": "C1", "question": "🔟 з 1️⃣2️⃣\nWhat is a synonym for 'ubiquitous'?", "options": ["omnipresent", "scarce", "unique", "rare"], "answer": "omnipresent"},
    # Добавьте еще 8 питань для C1
    {"level": "C2", "question": "1️⃣1️⃣ з 1️⃣2️⃣\nWhat is the meaning of 'laconic'?", "options": ["brief and to the point", "wordy", "verbose", "elaborate"], "answer": "brief and to the point"},
    {"level": "C2", "question": "1️⃣2️⃣ з 1️⃣2️⃣\nWhich word means 'clear and logical thinking'?", "options": ["lucid", "incoherent", "confused", "vague"], "answer": "lucid"},
    # Добавьте еще 8 питань для C2
]

teachers_data = {
    "Олена": {
        "text": "👩‍🏫 *Викладач Олена*\n\n"
                "Маю 4 років досвіду викладання англійської мови. Працюю з школярами та дітьми дошкільного віку, використовуючи інтерактивність.\n\n"
                "💬 Працюю з юними студентами, які хочуть покращити розмовні навички та почуватись впевненішими.\n\n"
                "🎥 Будемо вчити живу мову, дивитися TikTok/YouTube, розбирати улюблені серіали та треки.",
        "photo": "https://i.postimg.cc/JzsR8XP0/IMG-3209.jpg"
    },
    "Рода": {
        "text": "👩‍🏫 *Носійка Рода*\n\n"
                "I have over 1 year of experience teaching English as a second language, focusing on proficiency, basic language usage, and business communication.\n\n"
                "💬 I assist students aiming to improve their language proficiency, writing, and presentation skills, especially those preparing for IELTS and TOEFL.\n\n"
                "🎓 My lessons are dynamic, with real-life case studies and interactive methods to engage learners.",
        "photo": "https://i.postimg.cc/NFjW4hnF/image.jpg"
    },
    "Оля": {
        "text": "👩‍🏫 *Викладач Оля*\n\n"
                "Маю 7 років досвіду викладання англійської мови. Спеціалізуюсь на розмовній англійській та працюю як індивідуально, так і в групах.\n\n"
                "💬 Зі мною весело та продуктивно, завжди знаходжу підхід до студентів і мотивую їх до вивчення мови.\n\n"
                "📚 Використовую комунікативний підхід та допомагаю покращити англійську для роботи.",
        "photo": "https://i.postimg.cc/j5s9x0tc/image.jpg"
    },
   "Ярослав": {
    "text": "👨‍🏫 *Викладач Ярослав*\n\n"
            "Маю 2 роки досвіду викладання англійської мови 🇬🇧 для дорослих рівнів A1-B1. Мій підхід — це інтерактивність через фільми та серіали 🎬, що робить уроки цікавими!\n\n"
            "Я вмію знаходити спільну мову з усіма, особливо з хлопцями та чоловіками, якщо йдеться про футбол або інші 'чоловічі' теми. Завжди намагаюсь зробити навчання креативним і продуктивним!",
    "photo": "https://i.postimg.cc/rFdHF9XB/image.jpg"
},
    "Аня": {
        "text": "👩‍🏫 *Викладач Аня*\n\n"
                "Маю 1.5 року досвіду викладання англійської мови. Легко знаходжу контакт з різними віковими групами.\n\n"
                "🎓 Уроки проходять захопливо та результативно. Вмію пояснювати складні речі доступно.",
        "photo": "https://i.postimg.cc/8zQZkQbv/image.jpg"
    },
    "Христя": {
        "text": "👩‍🏫 *Викладач Христя*\n\n"
                "Маю 2 роки досвіду викладання англійської мови, спеціалізуюсь на розмовній та бізнес англійській.\n\n"
                "📚 Використовую комунікативний підхід, враховуючи особисті інтереси студентів для більшого залучення.",
        "photo": "https://i.postimg.cc/NGZ3Xn4s/image.jpg"
    },
    "Ольга": {
        "text": "👩‍🏫 *Викладач Ольга*\n\n"
                 "Маю 8 років досвіду викладання англійської мови. Працюю з розмовною та бізнес англійською.\n\n"
                 "💬 Мотивую студентів до самовдосконалення і завжди враховую їх інтереси на заняттях.",
        "photo": "https://i.postimg.cc/g2mBqb6W/image.jpg"
    }
}

def update_last_interaction(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name  # Имя пользователя
    last_name = message.chat.last_name  # Фамилия пользователя (может быть None)
    username = message.chat.username  # Имя пользователя в формате @username (может быть None)
    
    current_utc_time = datetime.now()
    local_time = current_utc_time.astimezone(local_timezone)
    readable_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
    current_time_unix = local_time.timestamp()
    
    # Обновляем запись в базе данных, добавляем имя, фамилию и username
    users_collection.update_one(
        {'user_id': chat_id},
        {'$set': {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'last_interaction': current_time_unix,
            'last_interaction_format': readable_time
        }},
        upsert=True
    )
    
    # Обновляем в локальной переменной для дальнейшего использования
    last_interaction_times[chat_id] = current_time_unix

#handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = States.WELCOME
    bot.send_message(message.chat.id, "👋 Привіт і ласкаво просимо до Hello Space! 🚀\n\n"
                                  "Ми раді, що ви вирішили розпочати свою подорож вивчення англійської мови разом з нами! 🇬🇧🌟"
                                 )
    video = open('video_2024-09-24_10-16-39.mp4', 'rb')
    bot.send_video(message.chat.id, video)
    video.close()
    
    send_main_menu(message, admins, bot, update_last_interaction)
    update_last_interaction(message)
    
@bot.message_handler(content_types=['photo', 'video'])
def handle_media_message(message):
    if message.chat.id in admins:
        if user_states.get(message.chat.id) == States.CONFIRM_SENDING_TO_USER:
            if message.content_type == 'photo':
                admin_news[message.chat.id] = {'photo': message.photo[-1].file_id}  # Сохраняем ID фото
                bot.send_message(message.chat.id, "Фото отримано. Тепер введіть текст для підпису до фото.")
                
                # Если видео
            elif message.content_type == 'video':
                admin_news[message.chat.id] = {'video': message.video.file_id}  # Сохраняем ID видео
                bot.send_message(message.chat.id, "Відео отримано. Тепер введіть текст для підпису до відео.")
                
            user_states[message.chat.id] = "AWAITING_CAPTION"
            
        elif user_states.get(message.chat.id) == States.CONFIRM_SENDING_TO_ALL:
            if message.content_type == 'photo':
                admin_news[message.chat.id] = {'photo': message.photo[-1].file_id}  # Сохраняем ID фото
                bot.send_message(message.chat.id, "Фото отримано. Тепер введіть текст для підпису до фото.")
                
                # Если видео
            elif message.content_type == 'video':
                admin_news[message.chat.id] = {'video': message.video.file_id}  # Сохраняем ID видео
                bot.send_message(message.chat.id, "Відео отримано. Тепер введіть текст для підпису до відео.")
                
            user_states[message.chat.id] = "AWAITING_CAPTIONS"


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "AWAITING_CAPTION")
def collect_caption_for_media(message):
    if message.chat.id in admins:
        admin_news[message.chat.id]['text'] = message.text  # Сохраняем текст в ту же запись
        selected_user_id = selected_users.get(message.chat.id)
        bot.send_message(message.chat.id, 
                         f"Ви бажаєте надіслати новину користувачу з ID: {selected_user_id}? (Так/Ні)")
        user_states[message.chat.id] = "CONFIRM_SENDING"

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "AWAITING_CAPTIONS")
def collect_caption_for_media(message):
    if message.chat.id in admins:
        admin_news[message.chat.id]['text'] = message.text  # Сохраняем текст в ту же запись
        bot.send_message(message.chat.id, 
                         f"Ви бажаєте надіслати новину всім користувачам? (Так/Ні)")
        user_states[message.chat.id] = "CONFIRM_SENDING_TO_ALL_USERS"

@bot.callback_query_handler(func=lambda call: True)
def handle_welcome_response(call):
    update_last_interaction(call.message)
    if call.data == "enter_news":
        enter_news(call.message, bot, users_collection, States)
    elif call.data == "send_to_all":  # Новая логика для массовой рассылки
        bot.send_message(call.message.chat.id, "Введіть новину для розсилки всім користувачам:")
        user_states[call.message.chat.id] = "CONFIRM_SENDING_TO_ALL"  # Устанавливаем состояние
    elif call.data.startswith("choose_user_"):
        selected_user_id = int(call.data.split("_")[-1])
        selected_user = users_collection.find_one({'user_id': selected_user_id})
        
        if selected_user:
            first_name = selected_user.get('first_name', 'Невідоме ім\'я')
            last_name = selected_user.get('last_name', '')
            username = selected_user.get('username', 'Немає username')
            
            selected_users[call.message.chat.id] = selected_user_id
            bot.send_message(call.message.chat.id, 
                             f"Ви вибрали користувача:\n"
                             f"Ім'я: {first_name}\n"
                             f"Прізвище: {last_name}\n"
                             f"Username: @{username}\n"
                             f"ID: {selected_user_id}\n\n"
                             "Введіть новину для відправлення.")
            
            user_states[call.message.chat.id] = States.CONFIRM_SENDING_TO_USER
        else:
            bot.send_message(call.message.chat.id, "Користувач не знайдений.")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == States.CONFIRM_SENDING_TO_USER)
def collect_personal_news(message):
    if message.chat.id in admins:
        selected_user_id = selected_users.get(message.chat.id)
        if selected_user_id:
            # Если сообщение содержит ссылку на видео
            if "http" in message.text and ("youtube" in message.text or "drive.google" in message.text):
                admin_news[message.chat.id] = {'video_link': message.text}
                bot.send_message(message.chat.id, 
                                 f"Ви бажаєте надіслати новину користувачу з ID: {selected_user_id}? (Так/Ні)")
                user_states[message.chat.id] = "CONFIRM_SENDING"
            else:
                admin_news[message.chat.id] = {'text': message.text}
                bot.send_message(message.chat.id, 
                                 f"Ви бажаєте надіслати новину користувачу з ID: {selected_user_id}? (Так/Ні)")
                user_states[message.chat.id] = "CONFIRM_SENDING"
        else:
            bot.send_message(message.chat.id, "Не вибраний користувач для відправки новини.")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "CONFIRM_SENDING_TO_ALL")
def collect_news_for_all(message):
    if message.chat.id in admins:
        # Проверяем, если это текст или ссылка на видео
        if "http" in message.text and ("youtube" in message.text or "drive.google" in message.text):
            admin_news[message.chat.id] = {'video_link': message.text}
        else:
            admin_news[message.chat.id] = {'text': message.text}
        
        bot.send_message(message.chat.id, "Ви бажаєте надіслати новину всім користувачам? (Так/Ні)")
        user_states[message.chat.id] = "CONFIRM_SENDING_TO_ALL_USERS"

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "CONFIRM_SENDING")
def confirm_sending_news(message):
    if message.text.lower() == "так":
        selected_user_id = selected_users.get(message.chat.id)
        send_news_to_user(message.chat.id, selected_user_id, admin_news, bot)
    else:
        bot.send_message(message.chat.id, "Відправка новини скасована.")
    user_states[message.chat.id] = None

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "CONFIRM_SENDING_TO_ALL_USERS")
def confirm_sending_news_to_all(message):
    if message.text.lower() == "так":
        send_news_to_all(message.chat.id, admin_news, bot, users_collection)
    else:
        bot.send_message(message.chat.id, "Відправка новини скасована.")
    user_states[message.chat.id] = None


# @bot.message_handler(func=lambda message: message.text == "📊 Дізнатися свій рівень")
# def start_message(message):
#     bot.send_message(message.chat.id, "Welcome to the English Level Test! Please answer the questions by typing your answers.")
#     start_quiz(message, questions, user_answers, bot)

@bot.message_handler(func=lambda message: message.text == "🏫 Про Школу")
def start_message(message):
    about_school_menu(message, bot, update_last_interaction)

# @bot.message_handler(func=lambda message: message.chat.id in user_answers and user_answers[message.chat.id]['current_question'] < len(questions))
# def handle_answer(message):
#     user_id = message.chat.id
#     question_data = questions[user_answers[user_id]['current_question']]

#     # Проверка ответа (игнорируем регистр)
#     if message.text.strip().lower() == question_data['correct'].lower():
#         user_answers[user_id]['correct_count'] += 1

#     # Переход к следующему вопросу
#     user_answers[user_id]['current_question'] += 1
#     if user_answers[user_id]['current_question'] < len(questions):
#         send_question(message, questions, user_answers, bot)
#     else:
#         calculate_result(message, user_answers, questions, bot)
        
@bot.message_handler(func=lambda message: message.text == "🏠 Головне меню")
def handle_main_menu_request(message):
    chat_id = message.chat.id
    #user_last_interaction[chat_id] = datetime.now()
    send_main_menu(message, admins, bot, update_last_interaction)
    
@bot.message_handler(func=lambda message: message.text == "❓ Чому ми?")
def handle_main_menu_request(message):
    chat_id = message.chat.id
    #user_last_interaction[chat_id] = datetime.now()
    why_we(message, bot, update_last_interaction)
    
@bot.message_handler(func=lambda message: message.text == "💬 Популярні запитання")
def handle_main_menu_request(message):
    chat_id = message.chat.id
    #user_last_interaction[chat_id] = datetime.now()
    popular_question(message, bot, update_last_interaction)
    
@bot.message_handler(func=lambda message: message.text == "📚 Про навчання")
def handle_main_menu_request(message):
    chat_id = message.chat.id
    #user_last_interaction[chat_id] = datetime.now()
    learn_menu(message, bot, update_last_interaction)

@bot.message_handler(func=lambda message: message.text == "📚 Наші курси")
def handle_main_menu_request(message):
    chat_id = message.chat.id
    #user_last_interaction[chat_id] = datetime.now()
    course_structure(message, bot, update_last_interaction)

@bot.message_handler(func=lambda message: message.text == "🎓 Формати навчання")
def handle_main_menu_request(message):
    chat_id = message.chat.id
    #user_last_interaction[chat_id] = datetime.now()
    format_learn(message, bot, update_last_interaction)
    
@bot.message_handler(func=lambda message: message.text == "👩‍🏫 Наші викладачі")
def show_teachers_menu(message):
    teachers_menu(message, bot, update_last_interaction, teachers_data)

# Обработчик всех текстовых сообщений для обработки нажатий на кнопки
@bot.message_handler(func=lambda message: message.text in teachers_data)
def process_teacher_choice(message):
    handle_teacher_choice(message, bot, teachers_data)
    
  
@bot.message_handler(func=lambda message: message.text == "📍 Наші контакти")
def handle_main_menu_request(message):
    chat_id = message.chat.id
    #user_last_interaction[chat_id] = datetime.now()
    contacts(message, bot, update_last_interaction)
    send_main_menu(message, admins, bot, update_last_interaction)
    
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    contact = message.contact
    chat_id = message.chat.id

    # Сообщение в чат с контактом
    contact_message = (
        f"Новый контакт:\n"
        f"Имя: {contact.first_name}\n"
        f"Телефон: {contact.phone_number}\n"
        f"ID пользователя: {contact.user_id}\n"
        f"ID чата: {chat_id}"
    )

    bot.send_message(message.chat.id, "Дякую! Наші менеджери незабаром зв'яжуться з Вами.")

    bot.send_message(CONTACT_RECEIVER_CHAT_ID, contact_message)
    
@bot.message_handler(func=lambda message: message.text == "📊 Дізнатися свій рівень")
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton('Грамматика')
    item2 = types.KeyboardButton('Лексика')
    item3 = types.KeyboardButton('🏠 Головне меню')
    markup.add(item1, item2)
    markup.add(item3)
    bot.send_message(message.chat.id, "Привіт! Я бот для тестування твого рівня англійської мови. Вибери тест: Граматика чи Лексика.", reply_markup=markup)
    
# Обработчик тестов
@bot.message_handler(func=lambda message: message.text in ['Грамматика', 'Лексика'])
def start_test(message):
    chat_id = message.chat.id
    if message.text == 'Грамматика':
        user_data[chat_id] = {"questions": grammar_questions, "score": 0, "current_question": 0}
    elif message.text == 'Лексика':
        user_data[chat_id] = {"questions": vocabulary_questions, "score": 0, "current_question": 0}
    send_next_question(chat_id, user_data, bot, calculate_level)    
    
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def check_answer(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id)
    
    if user is None:
        return
    
    current_question = user["current_question"]
    questions = user["questions"]
    
    # Проверка правильности ответа
    if message.text == questions[current_question]["answer"]:
        user["score"] += 1
    
    # Если пользователь завершил тест
    if message.text == "Завершити тест":
        calculate_level(chat_id, user_data, bot)
        
        # Сброс данных после завершения теста
        reset_user_data(chat_id)
        
        return
    
    # Переход к следующему вопросу
    user["current_question"] += 1
    
    # Отправка следующего вопроса
    send_next_question(chat_id, user_data, bot, calculate_level)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global selected_course  # Используем глобальную переменную
    
    if message.text == "🌐 Загальний курс":
        selected_course = "general"  # Сохраняем выбор курса
        course_deteil(message, bot, update_last_interaction, course_type="general")
    elif message.text == "👤 Індивідуальний курс":
        selected_course = "indiv"
        course_deteil(message, bot, update_last_interaction, course_type="indiv")
    elif message.text == "👨‍🏫 Групові заняття діти":
        selected_course = "group_child"
        course_deteil(message, bot, update_last_interaction, course_type="group_child")
    elif message.text == "🗣️ Розмовний інтенсив":
        selected_course = "group_speak"
        course_deteil(message, bot, update_last_interaction, course_type="group_speak")
    elif message.text == "🏢 Корпоративне навчання":
        selected_course = "group_corp"
        course_deteil(message, bot, update_last_interaction, course_type="group_corp")
    
    # Если нажата кнопка "Ціна"
    elif message.text == "💰 Ціна" and selected_course:
        # Выводим цену для выбранного курса
        show_price(message, bot, update_last_interaction, course_type=selected_course)
    
    # Если нажата кнопка "Про курс"
    elif message.text == "📖 Про курс" and selected_course:
        # Выводим информацию о курсе для выбранного курса
        show_about_course(message, bot, update_last_interaction, course_type=selected_course)

# Функция для сброса данных пользователя
def reset_user_data(chat_id):
    if chat_id in user_data:
        user_data[chat_id]["current_question"] = 0  # Сбросить текущий вопрос
        user_data[chat_id]["score"] = 0  # Сбросить счет
        # Если хотите полностью удалить пользователя из данных
        # del user_data[chat_id]
    

# scheduler = BackgroundScheduler()
# scheduler.add_job(send_reminder, 'interval', seconds=10)
# scheduler.start()

bot.polling(none_stop=True)
