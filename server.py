from bonus_questions import SAMPLE_QUESTIONS
from flask import Flask, render_template, request, redirect, url_for, session
import data_manager
import connection
import datetime
import util

app = Flask(__name__)


#Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/")
@app.route('/list', methods=['GET'])
def list():
    if 'sort_by' in request.args and 'order' in request.args:
        sort_by = request.args['sort_by']
        order = request.args['order']

        table_data = data_manager.get_questions(sort_by, order)
        return render_template('list.html',
                               table_data=table_data,
                               sort_by=sort_by,
                               order=order)
    else:
        table_data = data_manager.get_questions()

        return render_template('list.html',
                               table_data=table_data)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():

    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        question = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    0,
                    0,
                    request.form['title'],
                    request.form['message'],
                    request.form['image']
                    ]
        data_manager.add_question(question)
        return redirect(url_for('list'))


@app.route('/display-question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    data_manager.update_question_view_number(question_id)

    answer_headers = data_manager.get_answer_column_names()
    the_question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)

    return render_template('display-question.html',
                           question_id=question_id,
                           the_question=the_question,
                           answers=answers,
                           answer_headers=answer_headers
                           )

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question_by_id(question_id)
    return redirect('/list')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    message = {}
    if request.method == 'GET':
        table_header = data_manager.table_header()
        the_question = data_manager.get_question(question_id)
        return render_template('new-answer.html',
                               table_header=table_header,
                               the_question=the_question,
                               question_id=question_id)
    elif request.method == 'POST':
        message['message'] = request.form['message']
        message['question_id'] = question_id
        data_manager.write_answer_data(message)
        return redirect('/display-question/' + question_id)



@app.route('/question/<question_id>/edit')
def edit_question(question_id):
    pass




@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_asnwer(answer_id):
    if request.method == 'GET':
        question_id = connection.get_question_id_by_answer_id(answer_id)

        data_manager.delete_answer_by_id(answer_id)

        return redirect('/display-question/' + question_id)


@app.route('/answer/<question_id>/<answer_id>/vote-up', methods=['GET', 'POST'])
def vote_up_answer(question_id, answer_id):
    answers = data_manager.all_answers_in_csv()
    if request.method == 'GET':
        for row in answers:
            if row['id'] == answer_id and row['question_id'] == question_id:
                row['vote_number'] = int(row['vote_number']) + 1
    data_manager.write_all_answers(answers)
    return redirect('/display-question/' + question_id)


@app.route('/question/<question_id>/vote-up')
def vote_up_question(question_id):
    questions = data_manager.all_questions_in_csv()
    if request.method == 'GET':
        for row in questions:
            if row['id'] == question_id:
                row['vote_number'] = int(row['vote_number']) + 1
    data_manager.write_all_questions(questions)
    return redirect('/list')


''' User Registration part'''
@app.route('/registration', methods=["GET", "POST"])
def registration():
    user = {}
    if request.method == "POST":
        user['username'] = request.form['username']
        user['pasword'] = util.hash_password(request.form['password'])
        user['registration_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user['number_of_questions'] = 0
        user['number_of_answers'] = 0
        user['number_of_comments'] = 0
        user['reputation'] = 0

        data_manager.add_user(user)
        return redirect(url_for('list'))


'''User login page and authentication'''
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        original_password = data_manager.check_password(username)

        valid_password = util.verify_password(password, original_password)

        if valid_password:
            session['username'] = request.form['username']
            return redirect((url_for('list')))
        else:
            redirect(url_for('login'))
    return render_template('login.html')


if __name__ == "__main__":
    app.run(
        debug=True
    )




