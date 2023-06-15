import psycopg2
from psycopg2 import Error

db_name = 'diplom'
db_user = ''
db_password = ''

# Функция подключения к базе данных
def connect_database():
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password
        )
        return connection
    except (Exception, Error) as error:
        print('Error while connecting to PostgreSQL:', error)

# Функция создания таблицы слов в базе данных
def create_words_table(user_id):
    connection = connect_database()
    if connection:
        try:
            cursor = connection.cursor()
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {user_id}
                                    (id SERIAL PRIMARY KEY,
                                    user_id INTEGER,
                                    word TEXT,
                                    translation TEXT,
                                    example TEXT);'''
            cursor.execute(create_table_query)
            connection.commit()
            cursor.close()
            connection.close()
        except (Exception, Error) as error:
            print('Error while creating words table:', error)


# Функция заполнения базы данных общим набором слов
def fill_database_with_common_words(user_id):
    common_words = [
        ('color', 'цвет', 'This is a red color.'),
        ('car', 'машина', 'I drive a car.'),
        ('house', 'дом', 'I live in a house.'),
        ('dog', 'собака', 'She has a cute dog.'),
        ('cat', 'кошка', 'The cat is sleeping.'),
        ('book', 'книга', 'I am reading an interesting book.'),
        ('pen', 'ручка', 'I need a pen to write.'),
        ('friend', 'друг', 'He is my best friend.'),
        ('tree', 'дерево', 'The tree is tall.'),
        ('hello', 'привет','Hello, John! How are you?')
    ]

    connection = connect_database()
    if connection:
        try:
            cursor = connection.cursor()
            for word, translation, example in common_words:
                insert_query = f"INSERT INTO words (user_id, word, translation, example) VALUES ({user_id}, '{word}', '{translation}', '{example}');"
                cursor.execute(insert_query)
            connection.commit()
            cursor.close()
            connection.close()
        except (Exception, Error) as error:
            print('Error while filling database with common words:', error)

# Функция получения случайного слова из базы данных
def get_random_word(user_id):
    connection = connect_database()
    if connection:
        print('connect random')
        try:
            cursor = connection.cursor()
            select_query = f"SELECT * FROM words WHERE user_id = {int(user_id)} ORDER BY random() LIMIT 1;"

            cursor.execute(select_query)
            word_data = cursor.fetchone()
            print(word_data)
            cursor.close()
            connection.close()

            if word_data:
                word_id, _, word, translation, example = word_data
                return word_id, word, translation, example
            else:
                return None
        except (Exception, Error) as error:
            print('Error while getting random word from database:', error)


# Функция добавления нового слова в базу данных
def add_word(user_id, word, translation, example):
    connection = connect_database()
    if connection:
        try:
            cursor = connection.cursor()
            example = example.replace("'", "")
            insert_query = f"INSERT INTO words (user_id, word, translation, example) VALUES ({user_id}, '{word}', '{translation}', '{example}');"
            cursor.execute(insert_query)
            connection.commit()
            cursor.close()
            connection.close()
        except (Exception, Error) as error:
            print('Error while adding word to database:', error)


# Функция удаления слова из базы данных
def delete_word(user_id, word_id):
    connection = connect_database()
    if connection:
        try:
            cursor = connection.cursor()
            delete_query = f"DELETE FROM words WHERE user_id = {user_id} AND id = {word_id};"
            cursor.execute(delete_query)
            connection.commit()
            cursor.close()
            connection.close()
        except (Exception, Error) as error:
            print('Error while deleting word from database:', error)

def get_word_by_text(user_id, word):
    connection = connect_database()
    if connection:
        try:
            cursor = connection.cursor()
            select_query = f"SELECT * FROM words WHERE user_id = {user_id} AND word = %s;"
            cursor.execute(select_query, (word,))
            word_data = cursor.fetchone()
            cursor.close()
            connection.close()

            return word_data
        except (Exception, Error) as error:
            print('Error while getting word data from database:', error)
    return None

# Функция получения количества слов пользователя
def get_word_count(user_id):
    connection = connect_database()
    if connection:
        try:
            cursor = connection.cursor()
            count_query = f"SELECT COUNT(*) FROM words WHERE user_id = {user_id};"
            cursor.execute(count_query)
            word_count = cursor.fetchone()[0]
            cursor.close()
            connection.close()

            return word_count
        except (Exception, Error) as error:
            print('Error while getting word count from database:', error)
    return 0
