from flask import Flask, url_for, redirect, session, request, render_template
from random import randint, shuffle
from db_scripts import get_after_question, get_quizes, check_answer
import os

def start_quiz(quiz_id):
    session['quiz_number'] = quiz_id
    session['question_id'] = 0
    session['right_answers'] = 0
    session['total'] = 0

def finish_quiz():
    session.clear()

def quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list=q_list)

def question_form(question):
    answers_list = [question[2], question[3], question[4], question[5]]
    shuffle(answers_list)
    return render_template('test.html', question=question[1], question_numb=question[0], answers_list=answers_list)

def save_answers():
    answer = request.form.get('ans_text')
    question_numb = request.form.get('quest_numb')
    session['question_id'] = question_numb
    session['total'] += 1
    if check_answer(question_numb, answer):
        session['right_answers'] += 1

def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        selected_quiz = request.form.get('quiz')
        start_quiz(selected_quiz)
        return redirect(url_for('test'))

def test():
    if not ('quiz_number' in session) or int(session['quiz_number']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        next_question = get_after_question(session['question_id'], session['quiz_number'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)

def result():
    if not ('right_answers' in session) or not ('total' in session):
        return redirect(url_for('index'))
    else:
        result = render_template('result.html', right=session['right_answers'], answers=session['total'])
        finish_quiz()
        return result


folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)

app.add_url_rule('/', 'index', index, methods = ['post', 'get'])
app.add_url_rule('/test', 'test', test, methods = ['post', 'get'])
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'jopa'

if __name__ == '__main__':
    app.run()