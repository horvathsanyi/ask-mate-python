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


'''ADD NEW QUESTION'''
@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        question = {
                    'user_id': data_manager.get_user_id(session['username']),
                    'submission_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'view_number': 0,
                    'vote_number': 0,
                    'title': request.form['title'],
                    'message': request.form['message'],
                    'image': request.form['image']
        }
        data_manager.add_question(question)
        return redirect(url_for('list'))

'''Display One Question'''
@app.route('/display-question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    data_manager.update_question_view_number(question_id)

    answer_headers = data_manager.get_answer_column_names()
    the_question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    print(answer_headers)
    return render_template('display-question.html',
                           question_id=question_id,
                           the_question=the_question,
                           answers=answers,
                           answer_headers=answer_headers
                           )


'''DELETE QUESTION'''
@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question_by_id(question_id)
    return redirect('/list')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    new_answer = {}
    if request.method == 'GET':
        answer_headers = data_manager.get_answer_column_names()
        the_question = data_manager.get_question_by_id(question_id)
        return render_template('new-answer.html',
                               answer_headers=answer_headers,
                               the_question=the_question,
                               question_id=question_id)
    elif request.method == 'POST':
        new_answer['submission_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_answer['vote_number'] = 0
        new_answer['message'] = request.form['message']
        new_answer['image'] = request.form['image']
        new_answer['question_id'] = question_id
        new_answer['user_id'] = data_manager.get_user_id(session['username'])
        data_manager.add_new_answer(new_answer)
        return redirect(url_for('display_question', question_id=question_id))



@app.route('/question/<question_id>/edit')
def edit_question(question_id):
    pass


'''DELETE ANSWER'''
@app.route('/display-question/<question_id>/delete/<answer_id>', methods=['GET', 'POST'])
def delete_answer(answer_id,question_id):
        data_manager.delete_answer_by_id(answer_id)
        return redirect(url_for('display_question',question_id=question_id))


'''VOTE UP ANSWER'''
@app.route('/answer/<question_id>/<answer_id>/vote-up', methods=['GET', 'POST'])
def vote_up_answer(question_id, answer_id):
    answers = data_manager.all_answers_in_csv()
    if request.method == 'GET':
        for row in answers:
            if row['id'] == answer_id and row['question_id'] == question_id:
                row['vote_number'] = int(row['vote_number']) + 1
    data_manager.write_all_answers(answers)
    return redirect('/display-question/' + question_id)


'''VOTE UP QUESTION'''
@app.route('/question/<question_id>/vote-up')
def vote_up_question(question_id):
    data_manager.up_vote_question(question_id)
    return redirect(request.referrer)


''' User Registration part'''
@app.route('/registration', methods=["GET", "POST"])
def registration():
    user = {}
    if request.method == "POST":
        user['username'] = request.form['username']
        user['password'] = util.hash_password(request.form['password'])
        user['registration_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user['num_of_questions'] = 0
        user['num_of_answers'] = 0
        user['num_of_comments'] = 0
        user['reputation'] = 0
        data_manager.add_registration(user)
        user['registration_id'] = data_manager.get_registration_id(user['password'])
        data_manager.add_user(user)
        session['username'] = user['username']
        return redirect(url_for('list'))

    return render_template('registration.html')


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


''' LOGOUT '''

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('list'))


''' List Users '''

@app.route('/list-users')
def list_users():
    users_table = data_manager.get_users()
    users_table_header = data_manager.get_users_table_header()

    return render_template('list_users.html',
                    users_table=users_table,
                    users_table_header=users_table_header)


if __name__ == "__main__":
    app.run(debug=True)




