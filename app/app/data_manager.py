import bcrypt
import connection
import time
import os

from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]
MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024


@database_common.connection_handler
def get_all_user_story(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question LEFT OUTER JOIN question_tag
        ON question.id = question_tag.question_id"""
    cursor.execute(query)
    return cursor.fetchall()


# def get_all_user_story():
#     return connection.read_from_question()

@database_common.connection_handler
def sort_stories(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_latest_5_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_question_id(cursor: RealDictCursor) -> list:
    query = """
        SELECT id
        FROM question
        """
    cursor.execute(query)
    return cursor.fetchall()


# def sort_stories():
#     lst = connection.read_from_question()
#     return sorted(lst, key=lambda i: i['submission_time'])


@database_common.connection_handler
def get_answers(cursor: RealDictCursor, idnum: int) -> list:
    query = f"""
        SELECT *
        FROM answer
        WHERE question_id = {idnum}"""
    cursor.execute(query)
    return cursor.fetchall()

# def get_answers(idnum):
#     id_lst = []
#     lst = connection.read_from_answer()
#     for row in lst:
#         if idnum == int(row['question_id']):
#             id_lst.append(row)
#     return id_lst

@database_common.connection_handler
def get_qustion(cursor: RealDictCursor, idnum: int) -> list:
    query = f"""
        SELECT *
        FROM question
        WHERE id = {idnum}"""
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def get_latest_question(cursor: RealDictCursor) -> list:
    query = f"""
        SELECT *
        FROM question
        ORDER BY id DESC
        LIMIT 1"""
    cursor.execute(query)
    return cursor.fetchone()

# def get_qustion(idnum):
#     lst = get_all_user_story()
#     for row in lst:
#         if idnum == int(row['id']):
#             return row

@database_common.connection_handler
def add_question(cursor: RealDictCursor, new_question_dict: dict) -> list:
    query = f"""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
        VALUES (DEFAULT, '{new_question_dict['view_number']}', '{new_question_dict['vote_number']}', '{new_question_dict['title']}', '{new_question_dict['message']}', '{new_question_dict['image']}', '{new_question_dict['user_id']}')
        """
    cursor.execute(query)


@database_common.connection_handler
def edit_question(cursor: RealDictCursor, question_dict: dict) -> list:
    query = f"""
        UPDATE question
        SET view_number = '{question_dict['view_number']}',
            vote_number = '{question_dict['vote_number']}',
            title = '{question_dict['title']}',
            message = '{question_dict['message']}',
            image = '{question_dict['image']}'
        WHERE id = '{question_dict['id']}'
        """
    cursor.execute(query)

# def add_question(new_question_dict):
#     questions = connection.read_from_question()
#     if_append = True
#     new_questions_list = []
#     for question in questions:
#         if question['id'] == new_question_dict['id']:
#             new_questions_list.append(new_question_dict)     # update old question
#             if_append = False
#         else:
#             new_questions_list.append(question)  # keep the old question
#     if if_append:
#         new_questions_list.append(new_question_dict)
#     connection.write_question_to_file(new_questions_list)

@database_common.connection_handler
def sort_questions(cursor: RealDictCursor, dickey: int, direction: str) -> list:
    query = f"""
        SELECT *
        FROM question
        ORDER BY {dickey} {direction}"""
    cursor.execute(query)
    return cursor.fetchall()

# def sort_questions(dickey='submission_time', direction=True):
#     lst = connection.read_from_question()
#     if dickey == 'id' or dickey == 'submission_time' or dickey == 'view_number' or dickey == 'vote_number':
#         return sorted(lst, key=lambda i: int(i[dickey]), reverse=direction)
#     else:
#         return sorted(lst, key=lambda i: str(i[dickey]), reverse=direction)


# def generate_answer_id():
#     id_list = []
#     lst = connection.read_from_answer()
#     for row in lst:
#         id_list.append(row['id'])
#     return int(id_list[-1]) + 1


def generate_answer(id_number):
    answer = {}
    answer['id'] = 'change_me'
    answer['submission_time'] = int(time.time())
    answer['vote_number'] = 0
    answer['question_id'] = id_number
    answer['message'] = ''
    answer['image'] = ''
    return answer

@database_common.connection_handler
def update_answers(cursor: RealDictCursor, answer_dict: dict) -> list:
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
        VALUES (DEFAULT, '{answer_dict['vote_number']}', '{answer_dict['question_id']}', '{answer_dict['message']}', '{answer_dict['image']}', {answer_dict['user_id']})
        """
    cursor.execute(query)


@database_common.connection_handler
def edit_answer_image(cursor: RealDictCursor, answer_dict: dict) -> list:
    query = f"""
            UPDATE answer
            SET image = '{answer_dict['image']}'
            WHERE id = {answer_dict['id']}
            """
    cursor.execute(query)


# def update_answers(answer):
#     answers_list = connection.read_from_answer()
#     answers_list.append(answer)
#     connection.write_answer_to_file(answers_list)


### GET image URL by ID SQL


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, idnum: int) -> list:
    query = f"""
        DELETE FROM question
        WHERE id = {idnum}"""
    cursor.execute(query)


# def delete_question(idnum):
#     lst = connection.read_from_question()
#     newlst = []
#     for row in lst:
#         if int(row['id']) != idnum:
#             newlst.append(row)
#         else:
#             connection.delete_image(row['image'])
#     connection.write_question_to_file(newlst)


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, idnum: int) -> list:
    query = f"""
        DELETE FROM answer
        WHERE id = {idnum}"""
    cursor.execute(query)

# def delete_answer(idnum):
#     lst = connection.read_from_answer()
#     newlst = []
#     for row in lst:
#         if int(row['id']) != idnum:
#             newlst.append(row)
#         else:
#             connection.delete_image(row['image'])
#     connection.write_answer_to_file(newlst)


@database_common.connection_handler
def vote_question(cursor: RealDictCursor, idnum: int, vote: str) -> list:
    if vote == 'UP':
        diff = 1
    else:
        diff = -1
    query = f"""
        UPDATE question
        SET vote_number = vote_number + {diff}
        WHERE id = '{idnum}'
        """
    cursor.execute(query)


# def vote_question(idnum,vote):
#     lst = connection.read_from_question()
#     for row in lst:
#         if int(row['id']) == idnum:
#             if vote == 'UP':
#                 row['vote_number'] = int(row['vote_number']) + 1
#             elif vote == 'DOWN':
#                 row['vote_number'] = int(row['vote_number']) - 1
#     connection.write_question_to_file(lst)


@database_common.connection_handler
def vote_answer(cursor: RealDictCursor, idnum: int, vote: str) -> list:
    if vote == 'UP':
        diff = 1
    else:
        diff = -1
    query = f"""
        UPDATE answer
        SET vote_number = vote_number + {diff}
        WHERE id = '{idnum}'
        """
    cursor.execute(query)


# def vote_answer(idnum,vote):
#     lst = connection.read_from_answer()
#     for row in lst:
#         if int(row['id']) == idnum:
#             if vote == 'UP':
#                 row['vote_number'] = int(row['vote_number']) + 1
#             elif vote == 'DOWN':
#                 row['vote_number'] = int(row['vote_number']) - 1
#     connection.write_answer_to_file(lst)


# IMAGE UPLOADER START

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in ALLOWED_IMAGE_EXTENSIONS:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= MAX_IMAGE_FILESIZE:
        return True
    else:
        return False


def image_handler(idnum, question_or_answer, image):
    if image.filename == "":  # ERROR MESSAGE
        print("No filename")  # ERROR MESSAGE
    elif allowed_image(image.filename):
        new_filename = str(idnum)
        extension = str(image.filename).split('.')[-1]
        filename = new_filename + '.' + extension
        file_path = connection.upload_image(image, question_or_answer, filename)
        print(file_path)
        print(image)
        return file_path
    else:
        print("That file extension is not allowed")  # ERROR MESSAGE
        return ''

# IMAGE UPLOADER END

@database_common.connection_handler
def search_question(cursor: RealDictCursor, search_phrase: str) -> list:
    query = f"""
        SELECT *
        FROM question 
        WHERE title LIKE '%{ search_phrase }%' OR message LIKE '%{ search_phrase }%' """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def search_answer(cursor: RealDictCursor, search_phrase: str) -> list:
    query = f"""
        SELECT *
        FROM answer 
        WHERE message LIKE '%{ search_phrase }%' """
    cursor.execute(query)
    return cursor.fetchall()


def make_directory():
    try:
        os.makedirs('static/uploads/questions_images')
        os.makedirs('static/uploads/answers_images')
    except FileExistsError:
        pass

@database_common.connection_handler
def add_comment_to_question(cursor: RealDictCursor, question_id: int, comment: str, user_id: int) -> list:
    query = f"""
        INSERT INTO comment (question_id, message, submission_time, edited_number, user_id) 
        VALUES ({question_id}, '{comment}', DEFAULT, DEFAULT, {user_id})
        """
    cursor.execute(query)


@database_common.connection_handler
def get_question_comments(cursor: RealDictCursor, idnum: int) -> list:
    query = f"""
        SELECT message, submission_time, edited_number, id
        FROM comment
        WHERE question_id = {idnum}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_comment_to_answer(cursor: RealDictCursor, answer_id: int, comment: str, user_id: int) -> list:
    query = f"""
        INSERT INTO comment (answer_id, message, submission_time, edited_number, user_id) 
        VALUES ({answer_id}, '{comment}', DEFAULT, DEFAULT, {user_id})
        """
    cursor.execute(query)


@database_common.connection_handler
def get_answer_comments(cursor: RealDictCursor, idnum: int) -> list:
    query = f"""
        SELECT message, submission_time, edited_number, answer_id, id
        FROM comment
        WHERE answer_id = {idnum}"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_comment(cursor: RealDictCursor, idnum: int) -> list:
    query = f"""
        SELECT *
        FROM comment
        WHERE id = {idnum}"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def edit_comment(cursor: RealDictCursor, comment_dict: dict) -> list:
    query = f"""
        UPDATE comment
        SET message = '{comment_dict['message']}',
            submission_time = DEFAULT,
            edited_number = edited_number + 1
        WHERE id = '{comment_dict['id']}'
        """
    cursor.execute(query)

@database_common.connection_handler
def get_one_answer(cursor: RealDictCursor, answer_id: int) -> list:
    query = f"""
        SELECT *
        FROM answer
        WHERE id = {answer_id}
    """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def delete_comment(cursor: RealDictCursor, idnum: int) -> list:
    query = f"""
        DELETE FROM comment
        WHERE id = {idnum}"""
    cursor.execute(query)


#### START TAG

@database_common.connection_handler
def link_tag_and_question(cursor: RealDictCursor, common_dict: dict) -> list:
    query = f"""
        INSERT INTO question_tag (question_id, tag_id)
        VALUES (
        {common_dict['question_id']},
        {common_dict['tag_id']}
        )
        """
    cursor.execute(query)

@database_common.connection_handler
def add_tag(cursor: RealDictCursor, new_tag_dict: dict) -> list:
    query = f"""
        INSERT INTO tag (id, name)
        VALUES (DEFAULT, '{new_tag_dict['name']}')
        """
    cursor.execute(query)

    latest_tag_id = get_latest_tag()['id']
    #print('LATEST T: ', latest_tag_id)
    common_dict = {'question_id': new_tag_dict['question_id'], 'tag_id': latest_tag_id}
    link_tag_and_question(common_dict)


@database_common.connection_handler
def edit_tag(cursor: RealDictCursor, tag_dict: dict) -> list:
    query = f"""
        UPDATE tag
        SET name = '{tag_dict['name']}',
        WHERE id = '{tag_dict['id']}'
        """
    cursor.execute(query)


@database_common.connection_handler
def get_tag(cursor: RealDictCursor, idnum: int) -> list:
    query = f"""
        SELECT *
        FROM tag
        WHERE id = {idnum}"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_tag_id(cursor: RealDictCursor, name: str) -> list:
    query = f"""
        SELECT id
        FROM tag
        WHERE name = '{name}'"""
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def join_question_with_tag(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
        SELECT tag.id, tag.name
        FROM question_tag LEFT OUTER JOIN tag
        ON question_tag.tag_id = tag.id
        WHERE question_id = {question_id}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_latest_tag(cursor: RealDictCursor) -> list:
    query = f"""
        SELECT id
        FROM tag
        ORDER BY id DESC
        LIMIT 1"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_all_tags(cursor: RealDictCursor) -> list:
    query = f"""
        SELECT *
        FROM tag
        ORDER BY id ASC
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags_usage(cursor: RealDictCursor) -> list:
    query = f"""
        SELECT COUNT(tag_id) AS tag_count, name AS tag_name
        FROM tag
        INNER JOIN question_tag qt on tag.id = qt.tag_id
        GROUP BY tag_name
        ORDER BY tag_count ASC
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_latest_answer(cursor: RealDictCursor) -> list:
    query = f"""
        SELECT id
        FROM answer
        ORDER BY id DESC
        LIMIT 1"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_question_tags(cursor: RealDictCursor, question_id: int) -> list:
    query = f"""
        SELECT tag_id 
        FROM question_tag
        WHERE question_id = {question_id}
        """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def delete_tag(cursor: RealDictCursor, question_id: int, tag_id: int) -> list:
    query = f"""
        DELETE FROM question_tag
        WHERE question_id = {question_id}
        AND tag_id = {tag_id}"""
    cursor.execute(query)

### TAG END

@database_common.connection_handler
def get_answer_by_id(cursor: RealDictCursor, answer_id: int) -> list:
    query = f"""
        SELECT *
        FROM answer
        WHERE id = {answer_id}"""
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def edit_answer_message(cursor: RealDictCursor, answer_id: int, message: str) -> list:
    query = f"""
            UPDATE answer
            SET message = '{message}'
            WHERE id = {answer_id}
            """
    cursor.execute(query)


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def add_new_user(cursor: RealDictCursor, username: str, hashed_password: str) -> list:
    query = f"""
            INSERT INTO users(username, password, reputation)
            VALUES ('{username}', '{hashed_password}', 0)
            """
    cursor.execute(query)


@database_common.connection_handler
def get_all_user(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM users
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def count_questions(cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
            SELECT COUNT(*)
            FROM question
            WHERE user_id = {user_id}
            """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def count_answers(cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
            SELECT COUNT(*)
            FROM answer
            WHERE user_id = {user_id}
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def count_comments(cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
            SELECT COUNT(*)
            FROM comment
            WHERE user_id = {user_id}
            """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def answer_accept(cursor: RealDictCursor, answer_id: int) -> list:
    query = f"""
            UPDATE ANSWER
            SET accepted = TRUE
            WHERE id = {answer_id}
            """
    cursor.execute(query)
    return cursor.execute(query)

@database_common.connection_handler
def answer_unaccept(cursor: RealDictCursor, answer_id: int) -> list:
    query = f"""
                UPDATE ANSWER
                SET accepted = FALSE
                WHERE id = {answer_id}
                """
    cursor.execute(query)
    return cursor.execute(query)


@database_common.connection_handler
def get_questions_for_user(cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
            SELECT *
            FROM question
            WHERE user_id = {user_id}
            """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_answers_for_user(cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
            SELECT *
            FROM answer
            WHERE user_id = {user_id}
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_for_user(cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
            SELECT *
            FROM comment
            WHERE user_id = {user_id}
            """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def reputation_question(cursor: RealDictCursor, user_id: int, vote: str) -> list:
    if vote == 'UP':
        diff = 5
    else:
        diff = -2
    query = f"""
        UPDATE users
        SET reputation = reputation + {diff}
        WHERE id = {user_id}
        """
    cursor.execute(query)

@database_common.connection_handler
def reputation_answer(cursor: RealDictCursor, user_id: int, vote: str) -> list:
    if vote == 'UP':
        diff = 10
    else:
        diff = -2
    query = f"""
        UPDATE users
        SET reputation = reputation + {diff}
        WHERE id = {user_id}
        """
    cursor.execute(query)

@database_common.connection_handler
def reputation_answer_accept(cursor: RealDictCursor, user_id: int) -> list:
    query = f"""
        UPDATE users
        SET reputation = reputation + 15
        WHERE id = {user_id}
        """
    cursor.execute(query)
