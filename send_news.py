from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Функция начала ввода новостей
def enter_news(message, bot, users_collection, user_states, States):
    chat_id = message.chat.id
    user_states[chat_id] = States.ENTERING_NEWS
    bot.edit_message_text("Будь ласка, виберіть користувача для відправки новини:", chat_id, message.message_id)
    send_user_list(chat_id, bot, users_collection)
    

# Функция отправки списка пользователей
def send_user_list(admin_chat_id, bot, users_collection):
    users = users_collection.find()
    markup = InlineKeyboardMarkup()
    
    for user in users:
        user_id = user.get('user_id')
        first_name = user.get('first_name', 'Без імені')
        last_name = user.get('last_name', '')
        username = user.get('username', 'Без імені користувача')
        user_display = f"{first_name} {last_name} (@{username}) - ID: {user_id}"
        user_button = InlineKeyboardButton(user_display, callback_data=f"choose_user_{user_id}")
        markup.add(user_button)
    
    bot.send_message(admin_chat_id, "Виберіть користувача для відправки новини:", reply_markup=markup)

# Функция отправки новостей конкретному пользователю
def send_news_to_user(admin_chat_id, user_id, admin_news, bot):
    news_data = admin_news.get(admin_chat_id)
    if news_data and user_id:
        try:
            if 'video_link' in news_data:
                bot.send_message(user_id, f"🎥 Відео новина: {news_data['video_link']}")
            if 'photo' in news_data:
                bot.send_photo(user_id, news_data['photo'], caption=news_data.get('text', ''))
            elif 'video' in news_data:
                bot.send_video(user_id, news_data['video'], caption=news_data.get('text', ''))
            elif 'text' in news_data:
                bot.send_message(user_id, f"📰 Нова новина: {news_data['text']}")
            bot.send_message(admin_chat_id, f"Новина успішно відправлена користувачу з ID: {user_id}")
        except Exception as e:
            bot.send_message(admin_chat_id, f"Не вдалося надіслати повідомлення користувачу {user_id}: {e}")
    else:
        bot.send_message(admin_chat_id, "Сталася помилка при отриманні новини або користувача.")

# Функция массовой рассылки новостей всем пользователям
def send_news_to_all(admin_chat_id, admin_news, bot, users_collection):
    news_data = admin_news.get(admin_chat_id)
    if news_data:
        users = users_collection.find()
        for user in users:
            user_id = user.get('user_id')
            try:
                if 'video_link' in news_data:
                    bot.send_message(user_id, f"🎥 Відео новина: {news_data['video_link']}")
                if 'photo' in news_data:
                    bot.send_photo(user_id, news_data['photo'], caption=news_data.get('text', ''))
                elif 'video' in news_data:
                    bot.send_video(user_id, news_data['video'], caption=news_data.get('text', ''))
                elif 'text' in news_data:
                    bot.send_message(user_id, f"📰 Нова новина: {news_data['text']}")
                bot.send_message(admin_chat_id, f"Новина успішно відправлена користувачу з ID: {user_id}")
            except Exception as e:
                bot.send_message(admin_chat_id, f"Не вдалося надіслати повідомлення користувачу {user_id}: {e}")
    else:
        bot.send_message(admin_chat_id, "Сталася помилка при отриманні новини.")
