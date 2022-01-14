import connection
from datetime import datetime
from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@connection.connection_handler
def get_questions(cursor, sort_by="submission_time", order="ASC"):
    query = sql.SQL( """
        SELECT *
        FROM question   
        ORDER BY {sort_by} {order};
        """ ).format(sort_by=sql.Identifier(sort_by), order=sql.SQL(order))
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_id(cursor, question_id):
    query = sql.SQL("""
    SELECT *
    FROM question
    WHERE id = {question_id}
     """).format(question_id=sql.Literal(question_id))
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    query = sql.SQL("""
    SELECT *
    FROM answer
    WHERE question_id = {question_id}
     """).format(question_id=sql.Literal(question_id))
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_answer_column_names(cursor):
    query = ("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'answer' AND column_name  NOT IN ('question_id');
    """)
    cursor.execute(query)
    return cursor.fetchall()

''' ADD NEW QUESTION'''
@connection.connection_handler
def add_question(cursor, question):
    query = sql.SQL("""
    INSERT INTO question (id, user_id, submission_time, view_number, vote_number, title, message, image) 
    VALUES (DEFAULT, {user_id}, {submission_time}, {view_number}, {vote_number}, {title}, {message}, {image});
    """).format(user_id=sql.Literal(question['user_id']),
                submission_time=sql.Literal(question['submission_time']),
                view_number=sql.Literal(question['view_number']),
                vote_number=sql.Literal(question['vote_number']),
                title=sql.Literal(question['title']),
                message=sql.Literal(question['message']),
                image=sql.Literal(question['image'])
                )
    cursor.execute(query)


'''ADD NEW ANSWER'''
@connection.connection_handler
def add_new_answer(cursor, new_answer):
    query = sql.SQL("""
    INSERT INTO answer (id, submission_time, vote_number, question_id, message, image, user_id)
    VALUES (DEFAULT, {submission_time}, {vote_number}, {question_id}, {message}, {image}, {user_id})
    """).format(submission_time=sql.Literal(new_answer['submission_time']),
                vote_number=sql.Literal(new_answer['vote_number']),
                question_id=sql.Literal(new_answer['question_id']),
                message=sql.Literal(new_answer['message']),
                image=sql.Literal(new_answer['image']),
                user_id=sql.Literal(new_answer['user_id'])
                )
    cursor.execute(query)

'''UPDATE QUESTION VOTE NUMBER'''
@connection.connection_handler
def up_vote_question(cursor, question_id):
    query = sql.SQL("""
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = {question_id}
    """).format(question_id=sql.Literal(question_id))
    cursor.execute(query)


'''UPDATE QUESTION VIEW NUMBER'''
@connection.connection_handler
def update_question_view_number(cursor, question_id):
    query = sql.SQL("""
    UPDATE question 
    SET view_number = view_number+1
    WHERE id = {question_id}
    """).format(question_id=sql.Literal(question_id))
    return cursor.execute(query)


'''DELETE QUESTION'''
@connection.connection_handler
def delete_question_by_id(cursor, question_id):
    query = sql.SQL("""
    DELETE FROM question
    WHERE id = {question_id};
     """).format(question_id=sql.Literal(question_id));
    return cursor.execute(query)


'''DELETE ANSWER'''
@connection.connection_handler
def delete_answer_by_id(cursor,answer_id):
    query = sql.SQL("""
    DELETE FROM answer
    WHERE id = {answer_id}
    """).format(answer_id=sql.Literal(answer_id))
    cursor.execute(query)


''' Add user '''
@connection.connection_handler
def add_user(cursor, user):
    query = sql.SQL("""
    INSERT INTO "user" (id, registration_id, name, registration_date, num_of_questions, num_of_answers, num_of_comments, reputation) 
    VALUES (DEFAULT, {registration_id}, {name}, {registration_date}, {num_of_questions}, {num_of_answers}, {num_of_comments}, {reputation})
    """).format(registration_id=sql.Literal(user['registration_id']),
                name=sql.Literal(user['username']),
                registration_date=sql.Literal(user['registration_date']),
                num_of_questions=sql.Literal(user['num_of_questions']),
                num_of_answers=sql.Literal(user['num_of_answers']),
                num_of_comments=sql.Literal(user['num_of_comments']),
                reputation=sql.Literal(user['reputation'])
                )
    cursor.execute(query)

''' Add user registration '''
@connection.connection_handler
def add_registration(cursor, user):
    query = sql.SQL("""
    INSERT INTO registration (id, name, password) 
    VALUES (DEFAULT, {name}, {password})
    """).format(name=sql.Literal(user['username']),
                password=sql.Literal(user['password']),
                )
    cursor.execute(query)


''' Get registration ID'''
@connection.connection_handler
def get_registration_id(cursor, password):
    query = sql.SQL("""
    SELECT id
    FROM registration
    WHERE password = {password}
    """).format(password=sql.Literal(password))
    cursor.execute(query)
    return cursor.fetchone()['id']


''' GET USER ID'''
@connection.connection_handler
def get_user_id(cursor, username):
    query = sql.SQL("""
    SELECT id
    FROM "user"
    WHERE name = {username}
    """).format(username=sql.Literal(username))
    cursor.execute(query)
    return cursor.fetchone()['id']

''' User login '''
@connection.connection_handler
def check_password(cursor, username):
    query = sql.SQL("""
    SELECT password
    FROM registration
    WHERE name = {username}
    """).format(username=sql.Literal(username))
    cursor.execute(query)
    return cursor.fetchone()['password']


''' List Users '''
@connection.connection_handler
def get_users(cursor):
    query = """
    SELECT name, registration_date, num_of_questions, num_of_answers, num_of_comments, reputation
    FROM "user"
    """
    cursor.execute(query)
    return cursor.fetchall()


''' GET USERS TABLE COLUMN NAMES'''
@connection.connection_handler
def get_users_table_header(cursor):
    query = """
    SELECT name, registration_date, num_of_questions, num_of_answers, num_of_comments, reputation
    FROM "user"
    LIMIT 0
    """
    cursor.execute(query)
    colnames = [desc[0] for desc in cursor.description]
    return colnames


''' User details '''

@connection.connection_handler
def user_details(cursor, user_id):
    query = sql.SQL("""
    SELECT id, name, registration_date, num_of_questions, num_of_answers, num_of_comments, reputation
    FROM "user"
    WHERE id = {user_id}
    """).format(user_id=sql.Literal(user_id))
    cursor.execute(query)
    return cursor.fetchall()


''' User id '''

@connection.connection_handler
def user_id(cursor, username):
    query = sql.SQL("""
    SELECT id
    FROM "user"
    WHERE name = {username}
    """).format(username=sql.Literal(username))
    cursor.execute(query)
    return cursor.fetchone()['id']



# @connection.connection_handler
# def add_answer_to_question(cursor, question_id):
#     query = sql.SQL("""
#     INSERT INTO answer
#     WHERE id = {question_id}
#      """).format(question_id=sql.Literal(question_id));
#     cursor.execute(query)
#     return cursor.fetchall()






















# def table_header():
#     header = [key for key in connection.read_questions_csv()[0].keys()]
#     return [item.replace('_', ' ').title() for item in header]
#
#
# def table_data(sort='submission_time', order='asc'):
#     questions = connection.read_questions_csv()
#     ordering = False
#     if order == 'asc':
#         ordering = False
#     else:
#         ordering = True
#     if sort in ['title', 'message']:
#         sorted_questions = sorted(questions, key=lambda x: x[sort], reverse=ordering)
#     else:
#         sorted_questions = sorted(questions, key=lambda x: int(x[sort]), reverse=ordering)
#     return sorted_questions
#
#
# def get_question(id):
#     for row in connection.read_questions_csv():
#         if row['id'] == id:
#             return row
#
#
# def get_answer(id):
#     answers_list = []
#     for row in connection.read_answers_csv():
#         if row['question_id'] == id:
#             answers_list.append(row)
#     return answers_list
#
#
# def answer_header():
#     header = [key for key in connection.read_answers_csv()[0].keys()]
#     return [item.replace('_', ' ').title() for item in header]
#
#
# # TODO, FIXME: generate_id(last_id)
#
# def generate_id():
#     return len(connection.read_questions_csv()) + 1
#
#
# def generate_asnwer_id():
#     return len(connection.read_answers_csv()) + 1
#
#
# def unix_timestamp():
#     now = datetime.now()
#     return int(datetime.timestamp(now))
#
#
# def write_data(dict):
#     message = dict
#     message['id'] = generate_id()
#     message['submission_time'] = unix_timestamp()
#     message['view_number'] = 0
#     message['vote_number'] = 0
#     message['image'] = None
#     return connection.write_question_csv(message)
#
#
# def write_answer_data(dict):
#     message = dict
#     message['id'] = generate_asnwer_id()
#     message['submission_time'] = unix_timestamp()
#     message['vote_number'] = 0
#     message['image'] = None
#     return connection.write_answer_csv(message)
#
#
# def get_question_by_id(questions: list, id:int) -> dict:
#     for question in questions:
#         if question['id'] == id:
#             return question
#     return None
#
#
# def delete_question_by_id(id):
#     # read questions from file
#     questions = connection.read_questions_csv()
#
#     # delete question
#     question_to_delete = get_question_by_id(questions, id)
#     if question_to_delete is not None:
#         questions.remove(question_to_delete)
#
#     # update questions file
#     connection.rewrite_question_csv(questions)
#
#
# def delete_answer_by_id(id):
#     answers = connection.read_answers_csv()
#     for row in answers:
#         if row['id'] == id:
#             answers.remove(row)
#     connection.rewrite_answer_csv(answers)
#
#
# def all_answers_in_csv() -> list:
#     return connection.read_answers_csv()
#
#
# def all_questions_in_csv():
#     return connection.read_questions_csv()
#
#
# def write_all_answers(data):
#     return connection.rewrite_answer_csv(data)
#
#
# def write_all_questions(data):
#     return connection.rewrite_question_csv(data)
