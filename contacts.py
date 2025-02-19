def contacts(message, bot, update_last_interaction):
    chat_id = message.chat.id
    # Escape underscores in Telegram usernames by wrapping them with code formatting using backticks
    bot.send_message(
        chat_id,
        "*📞 Контакти:*\n\n"
        "*Телеграм:* `@HelloSpace_english`\n"
        "*Телефон:* +380 50 262 44 50\n"
        "*Електронна пошта:* hellospacelviv@gmail.com\n"
        "*Вебсайт:* [hellospacelviv.com](https://hellospacelviv.com/)",
        parse_mode='Markdown'
    )
    update_last_interaction(message)
