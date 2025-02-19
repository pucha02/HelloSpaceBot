from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def learn_menu(message, bot, update_last_interaction):
    chat_id = message.chat.id
    markups = ReplyKeyboardMarkup(resize_keyboard=True)

    button_structure = KeyboardButton("📚 Наші курси")
    button_formats = KeyboardButton("🎓 Формати навчання")
    button_main_menu = KeyboardButton("🏠 Головне меню")
    
    markups.add(button_structure, button_formats)
    markups.add(button_main_menu)
    bot.send_message(chat_id, "Обирайте, що цікавить 👇", reply_markup=markups)
    update_last_interaction(message)
    
    
def format_learn(message, bot, update_last_interaction):
    chat_id = message.chat.id
    bot.send_message(chat_id, "*📚 Формати навчання:*\n\n*🔹 Офлайн:*\n• Живі заняття у комфортних класах з доступом до навчальних матеріалів. Це найкращий варіант для тих, хто цінує безпосередній контакт з викладачем та атмосферу аудиторії.\n• Можливість інтерактивної взаємодії з групою та викладачем під час занять.\n• Мотиваційний ефект від занурення у навчальне середовище.\n\n*🔹 Онлайн:*\n• Гнучкий графік навчання та можливість вчитися з будь-якого місця, де є інтернет.\n• Доступ до записів занять та електронних матеріалів, що дозволяє повторювати та закріплювати вивчене в зручний час.\n• Інтерактивне навчання через сучасні онлайн-платформи з можливістю задавати питання в режимі реального часу.\n\n*🔹 Групове навчання:*\n• Спілкування з однодумцями та обмін досвідом у групі.\n• Мотивація через навчання у колективі, де всі учасники підтримують один одного.\n• Оптимальний вибір для тих, хто любить працювати в команді.\n\n*🔹 Індивідуальне навчання:*\n• Персоналізований підхід з урахуванням вашого рівня знань та цілей.\n• Гнучкість у виборі темпів та графіку навчання.\n• Максимальна увага викладача до ваших потреб.", parse_mode='Markdown')
    update_last_interaction(message)


def course_structure(message, bot, update_last_interaction):
    chat_id = message.chat.id
    markups = ReplyKeyboardMarkup(resize_keyboard=True)
    
    button_general = KeyboardButton("🌐 Загальний курс")
    button_indiv = KeyboardButton("👤 Індивідуальний курс")
    button_group_child = KeyboardButton("👨‍🏫 Групові заняття діти")
    button_group_speak = KeyboardButton("🗣️ Розмовний інтенсив")
    button_group_corp = KeyboardButton("🏢 Корпоративне навчання")
    button_formats = KeyboardButton("🎓 Формати навчання")
    button_main_menu = KeyboardButton("🏠 Головне меню")
    
    markups.add(button_general, button_indiv, button_group_child, button_group_speak, button_group_corp)
    markups.add(button_main_menu)
    markups.add(button_formats)
    
    bot.send_message(chat_id, "Оберіть курс 👇", parse_mode='Markdown', reply_markup=markups)
    update_last_interaction(message)
    
def course_deteil(message, bot, update_last_interaction, course_type):
    chat_id = message.chat.id
    markups = ReplyKeyboardMarkup(resize_keyboard=True)
    
    button_about_course = KeyboardButton("📖 Про курс")
    button_price = KeyboardButton("💰 Ціна") 
    button_courses = KeyboardButton("📚 Наші курси")
    button_main_menu = KeyboardButton("🏠 Головне меню")
    
    markups.add(button_about_course, button_price)
    markups.add(button_courses)
    markups.add(button_main_menu)
    
    # Отправляем информацию в зависимости от выбранного курса
    if course_type == "general":
        bot.send_message(chat_id, "Інформація про загальний курс", reply_markup=markups, parse_mode='Markdown')
    elif course_type == "indiv":
        bot.send_message(chat_id, "Інформація про індивідуальний курс", reply_markup=markups, parse_mode='Markdown')
    elif course_type == "group_child":
        bot.send_message(chat_id, "Інформація про групові заняття для дітей", reply_markup=markups, parse_mode='Markdown')
    elif course_type == "group_speak":
        bot.send_message(chat_id, "Інформація про розмовний інтенсив", reply_markup=markups, parse_mode='Markdown')
    elif course_type == "group_corp":
        bot.send_message(chat_id, "Інформація про корпоративне навчання", reply_markup=markups, parse_mode='Markdown')
    
    update_last_interaction(message)
    
def show_price(message, bot, update_last_interaction, course_type):
    chat_id = message.chat.id
    
    if course_type == "general":
        bot.send_message(chat_id, "📚 *Формати навчання*\n\n"
    "💻 *Онлайн:*\n"
    "• 8 занять\n"
    "• 340 грн / заняття\n"
    "• Загальна ціна: 2720 грн\n\n"
    "🏫 *У школі:*\n"
    "• 8 занять\n"
    "• 350 грн / заняття\n"
    "• Загальна ціна: 2800 грн\n", parse_mode='Markdown')
        
    elif course_type == "indiv":
        bot.send_message(chat_id, "💰 *Ціна індивідуального курсу*:\n\n• Дорослі (онлайн) — від 480 грн за 1 заняття 🖥️\n• Дорослі (в школі) — від 560 грн за 1 заняття 🏫\n• Діти (4-13 років) — від 360 грн за 1 заняття 👧\n• Підлітки (14-17 років) — від 430 грн за 1 заняття 👦\n\nТривалість одного заняття — 60 хвилин ⏰", parse_mode='Markdown')

        
    elif course_type == "group_child":
        bot.send_message(chat_id, "🎓 *Групові уроки*\n\n"
    "🔹 Одне заняття: 60 хвилин\n"
    "💵 Вартість: 250 грн / заняття\n\n"
    "📦 *Пакет занять:*\n"
    "• 8 занять за 2000 грн\n", parse_mode='Markdown')
        
    elif course_type == "group_speak":
        bot.send_message(chat_id,  "🗓️ *Тривалість курсу: 2 місяці*\n\n"
    "💻 *Онлайн-заняття:*\n"
    "• 2 рази на тиждень по 80 хв\n"
    "💰 Вартість курсу: 5600 грн\n\n"
    "🎁 *Знижка 5% для наших студентів!*\n", parse_mode='Markdown')
        
    elif course_type == "group_corp":
        bot.send_message(chat_id, "📅 *Графік занять:*\n"
    "• 2 рази на тиждень по 90 хвилин\n"
    "🎁 Перше заняття безкоштовно!\n\n"
    "💻 *Онлайн:*\n"
    "• 8500 грн / місяць за 8 занять\n\n"
    "🏫 *Офлайн:*\n"
    "• 7900 грн / місяць за 8 занять\n\n"
    "📈 *Додатково:*\n"
    "• Безкоштовна консультація та тестування працівників\n", parse_mode='Markdown')
    
    update_last_interaction(message)
    
def show_about_course(message, bot, update_last_interaction, course_type):
    chat_id = message.chat.id
    
    if course_type == "general":
        bot.send_message(chat_id, "🎓 *Загальний курс — групове навчання*\n\n"
    "✨ Що включено:\n"
    "• Безкоштовне тестування та пробний урок\n\n"
    "👥 *Міні-група* до 6 людей\n"
    "• 80% розмовної практики, 20% теорії\n"
    "• 2 заняття на тиждень по 90 хв\n"
    "• Чат з викладачем для питань\n"
    "• Підтримка менеджера\n"
    "• Сертифікат у кінці курсу\n"
    "• Доступ до матеріалів та ресурсів безкоштовно\n\n"
    "🎁 *Подарунок:* розмовні клуби з носієм мови\n", parse_mode='Markdown')
        
    elif course_type == "indiv":
        bot.send_message(chat_id, "🎓 *Індивідуальний курс* включає:\n\n• 80% розмовної лексики, 20% лексики та граматики 🗣️\n• Програму, побудовану під ваші цілі та запити 📋\n• Можливість замороження занять ❄️\n• Сертифікат після завершення курсу 🎉\n• Інтерактивні вправи та ігри для покращення успіхів у навчанні 🎮📈", parse_mode='Markdown')

        
    elif course_type == "group_child":
        bot.send_message(chat_id, "🎓 *Групові заняття для дітей*\n\n"
    "📝 *Ви отримаєте:*\n"
    "• Навчання у міні-групі\n"
    "• Підібрану групу до рівня дитини\n"
    "• Система мотивації\n"
    "• Інтерактивні вправи та ігри\n"
    "• Покращення успіхів у навчанні\n\n", parse_mode='Markdown')
        
    elif course_type == "group_speak":
        bot.send_message(chat_id, """
*Чому саме цей курс?*

• 📚 *Формат курсу:* flipped classroom  
• 🗣️ *2 місяці спілкування з носієм мови*  
• ✍️ *Insight notes*  
• 📰 *Статті, відео та аудіо матеріали* для кожної теми + словничок  
• 🤝 *Підтримка та ком'юніті з однодумцями*

*Flipped classroom*  
У цій моделі ви спочатку переглядаєте уроки або читаєте матеріали вдома, а потім на занятті працюєте над завданнями і обговореннями з вчителем та одногрупниками. Такий підхід допоможе вам краще засвоїти матеріал і використати час у класі більш ефективно.
""", parse_mode='Markdown')

        
    elif course_type == "group_corp":
        bot.send_message(chat_id, "📚 *Корпоративне навчання англійської мови* 🌍 має багато переваг: підвищення продуктивності 💼, полегшення роботи з клієнтами та партнерами з інших країн 🤝, а також відкриття нових кар'єрних можливостей 🚀.\n\n👥 *Спільне вивчення англійської* об'єднує працівників навколо досягнення цілей компанії 🏆. На заняттях вони спілкуються 🗣️, виконують завдання та працюють у групах, розвиваючи командну роботу 🤝.\n\n🧑‍🤝‍🧑 *Результат*: працівникам набагато легше організуватись для виконання завдань компанії 🎯.\n\n🔎 *Як ми працюємо?*\n\n1️⃣ Знайомимось, проводимо консультацію та надсилаємо комерційну пропозицію.\n\n2️⃣ Виявляємо сильні та слабкі сторони, щоб налаштувати процес навчання індивідуально під кожного.\n\n3️⃣ Аналізуємо та стежимо за прогресом протягом усього навчання. Наприкінці семестру пишемо тест та отримуємо сертифікат, який підтверджує рівень знань.", parse_mode='Markdown')
    update_last_interaction(message)