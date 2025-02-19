def start_quiz(message, questions, user_answers, bot):
    user_id = message.chat.id
    user_answers[user_id] = {'current_question': 0, 'correct_count': 0}
    send_question(message, questions, user_answers, bot)

def send_question(message, questions, user_answers, bot):
    user_id = message.chat.id
    current_question = user_answers[user_id]['current_question']
    
    # Check to avoid accessing out-of-range questions
    if current_question < len(questions):
        question_data = questions[current_question]
        bot.send_message(user_id, question_data['question'])
    else:
        bot.send_message(user_id, "There are no more questions!")



def calculate_result(message, user_answers, questions, bot):
    user_id = message.chat.id
    score = user_answers[user_id]['correct_count']
    total_questions = len(questions)

    # Определение уровня
    if score == total_questions:
        level = 'Advanced (C1-C2)'
    elif score >= total_questions * 0.7:
        level = 'Upper-Intermediate (B2)'
    elif score >= total_questions * 0.4:
        level = 'Intermediate (B1)'
    else:
        level = 'Beginner (A1-A2)'

    bot.send_message(user_id, f'Your score: {score}/{total_questions}\nYour English level: {level}')
    del user_answers[user_id]
    
 