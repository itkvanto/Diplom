import random
from telebot import types, TeleBot
from translation import get_word_example,get_word_translation
from database import create_words_table,fill_database_with_common_words,get_random_word,get_word_count,add_word,get_word_by_text,delete_word

# Инициализация бота
token_bot = ''
bot = TeleBot(token_bot)


# Функция начала работы с ботом
@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    bot.send_message(cid, """Привет 👋 Давай попрактикуемся в английском языке. Тренировки можешь проходить в удобном для себя темпе. \nПричём у тебя есть возможность использовать тренажёр как конструктор и собирать свою собственную базу для обучения. \nДля этого воспрользуйся командами в меню.\nНу что, начнём ⬇️""")
    create_words_table(cid)
    fill_database_with_common_words(cid)
    userStep[cid] = 0
    ask_question(cid)

@bot.message_handler(commands=['game'])
def game(message):
    cid = message.chat.id
    create_words_table(cid)
    userStep[cid] = 0
    ask_question(cid)

# Функция задает пользователю вопрос
def ask_question(user_id):
    word_data = get_random_word(user_id)
    word_id, word, translation, example = word_data

    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [word]
    for _ in range(3):
        random_word_data = get_random_word(user_id)
        buttons.append(random_word_data[1])
    random.shuffle(buttons)
    markup.add(*buttons)

    bot.send_message(user_id, f"Выбери перевод слова: {translation}", reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(user_id, check_answer, word_id, word, example, translation)


def restart_question(user_id, word_id, word, example,translation):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [word]
    for _ in range(3):
        random_word_data = get_random_word(user_id)
        buttons.append(random_word_data[1])
    random.shuffle(buttons)
    markup.add(*buttons)

    bot.send_message(user_id, f"Выбери перевод слова: {translation}", reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(user_id, check_answer, word_id, word, example,translation)


# Функция проверки ответа пользователя
def check_answer(message, word_id, word, example,translation):
    user_id = message.chat.id
    user_answer = message.text.strip()
    if message.text == '/exit':
        bot.send_message(user_id, "На сегодня закончили!")
    elif user_answer.lower() == word.lower():
        bot.send_message(user_id, "Правильный ответ!")
        bot.send_message(user_id, f"Пример использования: {example}")
        ask_question(user_id)
    else:
        bot.send_message(user_id, "Неправильный ответ. Попробуйте еще раз.")
        restart_question(user_id, word_id, word, example,translation)


# Обработчик команды добавления нового слова
@bot.message_handler(func=lambda message: message.text == '/add_word')
def add_word_command(message):
    user_id = message.chat.id
    userStep[user_id] = 1
    bot.send_message(user_id, "Введите новое слово на английском языке:")

# Обработчик получения нового слова
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def save_new_word(message):
    user_id = message.chat.id
    word = message.text.strip().lower()


    translation = get_word_translation(word)
    example = get_word_example(word)

    if translation and example:
        add_word(user_id, word, translation, example)
        word_count = get_word_count(user_id)
        bot.send_message(user_id, f"Слово '{word}' успешно добавлено в ваш словарь. "
                                  f"Теперь вы изучаете {word_count} слов.")
        userStep[user_id] = 0
    else:
        bot.send_message(user_id, "Не удалось получить перевод или пример использования слова. "
                                  "Проверьте правильность ввода или попробуйте позже.")

    userStep[user_id] = 0

@bot.message_handler(func=lambda message: message.text == '/delete_word')
def delete_word_command(message):
    user_id = message.chat.id
    userStep[user_id] = 2
    bot.send_message(user_id, "Введите слово на английском языке, которое хотите удалить:")

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def delete_word_by_text(message):
    user_id = message.chat.id
    word = message.text.strip().lower()

    word_data = get_word_by_text(user_id, word)
    if word_data:
        word_id,user_id, word, translation,example = word_data
        delete_word(user_id, word_id)
        word_count = get_word_count(user_id)
        bot.send_message(user_id, f"Слово '{word}' удалено из вашего словаря. "
                                  f"Теперь вы изучаете {word_count} слов.")
    else:
        bot.send_message(user_id, f"Слово '{word}' не найдено в вашем словаре.")
    userStep[user_id] = 0


# Функция получения текущего шага пользователя
def get_user_step(user_id):
    if user_id in userStep:
        return userStep[user_id]
    else:
        return 0

if __name__ == '__main__':
    userStep = {}
    bot.polling(none_stop=True)