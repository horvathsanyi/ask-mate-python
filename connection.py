# Creates a decorator to handle the database connection/cursor opening/closing.
# Creates the cursor with RealDictCursor, thus it returns real dictionaries, where the column names are the keys.
import os

import psycopg2
import psycopg2.extras


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper




































# import csv
#
# # TODO: read_csv_file(...)

#
# def read_questions_csv():
#     list_of_questions = []
#     with open('sample_data/question.csv', 'r') as csv_file:
#
#         csv_reader = csv.DictReader(csv_file)
#
#         for line in csv_reader:
#             list_of_questions.append(line)
#
#     return list_of_questions
#
#
# def read_answers_csv():
#     list_of_answers = []
#     with open('sample_data/answer.csv', 'r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#
#         for line in csv_reader:
#             list_of_answers.append(line)
#
#     return list_of_answers
#
#
# def write_question_csv(dict):
#     header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
#     with open('sample_data/question.csv', 'a') as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=header)
#         csv_writer.writerow(dict)
#
#
# def write_answer_csv(dict):
#     header = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
#     with open('sample_data/answer.csv', 'a') as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=header)
#         csv_writer.writerow(dict)
#
# # TODO
# def write_csv(file, content, header):
#     pass
#
# def rewrite_question_csv(questions):
#     header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
#     with open('sample_data/question.csv','w') as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=header)
#         csv_writer.writeheader()
#         csv_writer.writerows(questions)
#
# def rewrite_answer_csv(answers):
#     header = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
#     with open('sample_data/answer.csv','w') as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=header)
#         csv_writer.writeheader()
#         csv_writer.writerows(answers)
#
# def get_question_id_by_answer_id(answer_id):
#     answers = read_answers_csv()
#     for answer in answers:
#         if answer['id'] == answer_id:
#             return answer['question_id']
#     return None