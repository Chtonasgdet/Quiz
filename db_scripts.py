import sqlite3
import io
from random import randint
db_name = 'quiz_upd.sqlite'
conn = None
cursor = None


def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()
    
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    do('''CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY, 
        question VARCHAR, 
        answer VARCHAR, 
        wrong1 VARCHAR, 
        wrong2 VARCHAR, 
        wrong3 VARCHAR)''')

    do('''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        from_ INTEGER,
        untill INTEGER)''')

    do('''CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY,
        question_id INTEGER,
        quiz_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id))''')
    close()

def add_questions():
    questions = []
    i = 1
    with io.open('list_questions.txt', 'r', encoding = 'utf-8') as file:
        for line in file:
            if line.find('?') != -1:
                symbol = line.find('?')
            else:
                symbol = line.find('.')
            spisok = []
            spisok.append(line[:symbol+1])
            line = tuple(spisok+line[symbol+3:len(line)-1].split(', '))
            questions.append(line)
            print(i, '-', len(line))
            i += 1
    print(questions)
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)''', questions)
    conn.commit()
    close()

def add_quizes():
    quizes = [
        ('Наука', ),
        ('Биология', ),
        ('Страны и не только', ),
        ('Животные', ),
        ('Всякое', )
    ]
    open()
    cursor.executemany('''INSERT INTO quiz(name) VALUES(?)''', quizes)
    conn.commit()
    close()

def add_content():
    open()
    cursor.execute('''PRAGMA foreign_keys = on''')
    add_answer = input('Добавить связь (y/n)')
    while add_answer != 'n':
        if add_answer == 'y':
            try:
                quiz_id = int(input('id викторины:'))
                question_id = int(input('id вопроса:'))
                cursor.execute('''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)''', [quiz_id, question_id])
                conn.commit()
            except ValueError:
                print('Пожалуйста, вводите только числа!')
            except:
                print('Такого id не существует!')
        else:
            print('Команда не распознана. Пожалуйста, введите существующую команду (y/n)')
        add_answer = input('Добавить связь (y/n)')
    close()

def get_after_question(question_id, quiz_id):
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM quiz_content, question
    WHERE quiz_content.question_id == question.id AND quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id
    '''
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result

def get_quizes():
    open()
    query = '''SELECT * FROM quiz ORDER BY id'''
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result

def random_quiz():
    open()
    cursor.execute('''SELECT quiz_id FROM quiz_content''')
    count = cursor.fetchall()
    result = count[randint(0, len(count)-1)][0]
    close()
    return count

def check_answer(question_numb, answer_):
    query = '''SELECT question.answer
            FROM quiz_content, question
            WHERE quiz_content.id = ?
            AND quiz_content.question_id = question.id
            '''
    open()
    cursor.execute(query, [str(question_numb)])
    result = cursor.fetchone()
    print(result)
    close()
    if result is None:
        return False
    else:
        if result[0] == answer_:
            return True
        else:
            return False

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()


def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')


def main():
    #clear_db()
    #create()
    #add_questions()
    #add_quizes()
    #add_content()
    #show_tables()
    print(get_after_question(2, 3))
    print(get_quizes())
    print(random_quiz())
    
if __name__ == '__main__':
    main()
