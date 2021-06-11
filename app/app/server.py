from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.templating import render_template_string
#import data_manager
from html import escape

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

click_counter = 1
@app.route("/")
def question_list():
    # user_stories = data_manager.get_latest_5_questions()
    # all_question_id = data_manager.get_all_question_id()
    # tags_dict = {}
    # for question_id_dict in all_question_id:
    #     question_id = question_id_dict['id']
    #     tags = data_manager.join_question_with_tag(question_id)
    #     if tags is not None:
    #         tags_dict[question_id] = []
    #         for tag in tags:
    #             tags_dict[question_id].append({'tag_id': tag.pop('id'), 'name': tag.pop('name')})
    # data_manager.make_directory()
    # if 'username' in session:
    #     username = session['username']
    #     return render_template('list.html', user_stories=user_stories, tags_dict=tags_dict, click=click_counter,
    #                            all_question=False, username=username)
    # return render_template('list.html', user_stories=user_stories, tags_dict=tags_dict, click=click_counter, all_question=False)
    return render_template('test.html')


@app.route('/question/<int:idnum>', methods=['GET','POST'])
def return_question(idnum):
    question = data_manager.get_qustion(idnum)
    answer_list = data_manager.get_answers(idnum)
    question_comment_list = data_manager.get_question_comments(idnum)

    lst = []
    for row in answer_list:
        answer_id = row['id']
        answer_comment_list = data_manager.get_answer_comments(answer_id)
        # print(answer_comment_list)
        lst = lst + answer_comment_list
    # print(lst)


    return render_template('answer.html', question=question, answer_list=answer_list, idnum=idnum, question_comment_list=question_comment_list, lst=lst)   # please let 'idnum=idnum'


@app.route('/add-question/', methods=['GET', 'POST'])
@app.route('/question/<int:idnum>/edit', methods=['GET', 'POST'])
def add_question(idnum=''):
    if idnum == '':
        #submission_time = int(time.time())
        question_data = {'id': '', 'view_number':0,'vote_number':0, 'title': '', 'message': ''}
    else:
        question_data = data_manager.get_qustion(idnum)  # GET QUESTION DATA
    return render_template('add-question.html', question_data=question_data)


@app.route('/handle_question', methods=['POST', 'GET'])
def handle_question():
    if request.method == "POST":
        # get variables from the form:
        idnum = request.form['id']
        submission_time = request.form['submission_time']  # get variables from the form
        view_number = request.form['view_number']
        vote_number = request.form['vote_number']
        title = escape(request.form['title'])
        message = escape(request.form['message'])
        username = session['username']
        user_list = data_manager.get_all_user()
        for user in user_list:
            if username == user['username']:
                user_id = user['id']

        if idnum == "":   # if no idnum => this is a new question
            # get_max_idnum = max([int(row['id']) for row in data_manager.get_all_user_story()])
            # idnum = str(int(get_max_idnum) + 1)   # GET THE NEXT ID
            new_question_dict = {'id': idnum, 'submission_time': submission_time, 'view_number': view_number,
                                 'vote_number': vote_number, 'title': title, 'message': message, 'image': 'None', 'user_id': user_id}  # make the dictionary without picture
            data_manager.add_question(new_question_dict)
            latest_question = data_manager.get_latest_question()
            idnum = latest_question['id']
            # upload image start
            if request.files:
                image = request.files["image"]
                filename = data_manager.image_handler(idnum, 'question', image)
            # upload image end
                question_dict = {'id': idnum, 'submission_time': submission_time, 'view_number': view_number,
                             'vote_number': vote_number, 'title': title, 'message': message,
                             'image': filename, 'user_id': user_id}
                data_manager.edit_question(question_dict)
            return redirect('/')
        else:
            # upload image start
            if request.files:
                image = request.files["image"]
                filename = data_manager.image_handler(idnum, 'question', image)
            # upload image end
            question_dict = {'id': idnum, 'submission_time': submission_time, 'view_number': view_number,
                                 'vote_number': vote_number, 'title': title, 'message': message,
                                 'image': filename}
            data_manager.edit_question(question_dict)

        #import connection      # !!! THIS WOULD BE SHORTHER, but now it does not work... !!!
        #headers =connection.QUESTION_HEADER
        #new_question_dict = {header: request.form[header] for header in headers}    # make the dictionary

        return redirect('/question/' + idnum)


@app.route('/question/<int:idnum>/delete', methods=['POST'])
def delete_question(idnum):
    if request.method == 'POST':
        data_manager.delete_question(idnum)
        return redirect('/')


@app.route('/list', methods=['GET', 'POST'])
def sorting():
    global click_counter
    all_question_id = data_manager.get_all_question_id()
    tags_dict = {}
    for question_id_dict in all_question_id:
        question_id = question_id_dict['id']
        tags = data_manager.join_question_with_tag(question_id)
        if tags is not None:
            tags_dict[question_id] = []
            for tag in tags:
                tags_dict[question_id].append({'tag_id': tag.pop('id'), 'name': tag.pop('name')})
    user_stories = data_manager.sort_stories()
    if request.method == 'GET':
        dickey = request.args.get('order_by')
        if request.args.get('order_direction') == 'desc':
            direction = 'DESC'
        elif request.args.get('order_direction') == 'asc':
            direction = 'ASC'
        else:
            dickey = 'submission_time'
            direction = 'ASC'
        question_list = data_manager.sort_questions(dickey, direction)
        click_counter += 1
        return render_template('list.html', user_stories=question_list, tags_dict=tags_dict, click=click_counter)
    return render_template('list.html', user_stories=user_stories, tags_dict=tags_dict, click=click_counter, all_question=True)

# WHEN YOU CREATE EDIT ANSWER, DO NOT AS TIMESTAMP AS DEFAULT, LEAVE THIS FIELD
@app.route('/question/<int:idnum>/new-answer', methods=['GET','POST'])
def new_answer(idnum):
    question = data_manager.get_qustion(idnum)
    answers_list = data_manager.get_answers(idnum)
    answer = data_manager.generate_answer(idnum)

    username = session['username']
    user_list = data_manager.get_all_user()
    for user in user_list:
        if username == user['username']:
            user_id = user['id']

    if request.method == 'POST':
        answer['message'] = request.form['answer']
        answer['user_id'] = user_id

        data_manager.update_answers(answer)

        # upload image start
        if request.files:
            image = request.files["image"]
            answer['id'] = data_manager.get_latest_answer()['id']
            filename = data_manager.image_handler(answer['id'], 'answer', image)
            answer['image'] = filename
            data_manager.edit_answer_image(answer)
            #answer['image'] = filename
        # upload image end

        return redirect('/question/'+str(idnum))

    return render_template('new-answer.html', question=question, answers=answers_list, idnum=idnum)

@app.route('/question/<int:idnum>/vote_up', methods=['GET', 'POST'])
def vote_question_up(idnum):
    data_manager.vote_question(idnum, 'UP')
    question = data_manager.get_qustion(idnum)
    user_id = question['user_id']
    data_manager.reputation_question(user_id, 'UP')
    return redirect('/')

@app.route('/question/<int:idnum>/vote_down', methods=['GET', 'POST'])
def vote_question_down(idnum):
    data_manager.vote_question(idnum,'DOWN')
    question = data_manager.get_qustion(idnum)
    user_id = question['user_id']
    data_manager.reputation_question(user_id, 'DOWN')
    return redirect('/')

@app.route('/question/<int:idnum>/<int:answer_id>/vote_up', methods=['GET', 'POST'])
def vote_answer_up(idnum, answer_id):
    data_manager.vote_answer(answer_id, 'UP')
    question = data_manager.get_qustion(idnum)
    user_id = question['user_id']
    data_manager.reputation_answer(user_id, 'UP')
    return redirect('/question/'+str(idnum))

@app.route('/question/<int:idnum>/<int:answer_id>/vote_down', methods=['GET', 'POST'])
def vote_answer_down(idnum, answer_id):
    data_manager.vote_answer(answer_id,'DOWN')
    question = data_manager.get_qustion(idnum)
    user_id = question['user_id']
    data_manager.reputation_answer(user_id, 'DOWN')
    return redirect('/question/'+str(idnum))


@app.route('/answer/<int:answer_id>/delete/<int:idnum>', methods=['GET'])
def delete_answer(answer_id, idnum):
    if request.method == 'GET':
        data_manager.delete_answer(answer_id)
        return redirect(f'/question/{idnum}')


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    username = session['username']
    user_list = data_manager.get_all_user()
    for user in user_list:
        if username == user['username']:
            user_id = user['id']
    if request.method == 'POST':
        comment = request.form['comment']
        data_manager.add_comment_to_question(question_id, comment, user_id)
        return redirect(f'/question/{question_id}')
    return render_template('add-comment.html', question_id=question_id, type='question')


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    username = session['username']
    user_list = data_manager.get_all_user()
    for user in user_list:
        if username == user['username']:
            user_id = user['id']
    if request.method == 'POST':
        comment = request.form['comment']
        data_manager.add_comment_to_answer(answer_id, comment, user_id)
        answer = data_manager.get_one_answer(answer_id)
        return redirect(f'/question/{answer["question_id"]}')
    return render_template('add-comment.html', answer_id=answer_id, type='answer')

@app.route('/comment/<int:comment_id>/edit', methods=['GET','POST'])
def edit_comment(comment_id):
    comment_data = data_manager.get_comment(comment_id)
    if comment_data["question_id"] is not None:
        question_id = comment_data["question_id"]
    else:
        answer_id = comment_data['answer_id']
        answer_dict = data_manager.get_one_answer(answer_id)
        question_id = answer_dict["question_id"]
    if request.method == 'POST':
        message = request.form['comment']
        comment_dict = {'id': comment_id, 'message' : message}
        data_manager.edit_comment(comment_dict)
        return redirect(f'/question/{question_id}')
    return render_template("edit-comment.html", comment_text=comment_data['message'], comment_id=comment_id)

@app.route('/comments/<int:comment_id>/delete')
def delete_comment(comment_id):
    comment_data = data_manager.get_comment(comment_id)
    if comment_data["question_id"] is not None:
        question_id = comment_data["question_id"]
    else:
        answer_id = comment_data['answer_id']
        answer_dict = data_manager.get_one_answer(answer_id)
        question_id = answer_dict["question_id"]
    data_manager.delete_comment(comment_id)
    return redirect(f'/question/{question_id}')

@app.route('/search', methods=['GET'])
def search_phrase():
    all_question_id = data_manager.get_all_question_id()
    search_phrase = escape(request.args.get('search_phrase'))
    search_results = data_manager.search_question(search_phrase)
    search_result_answers = data_manager.search_answer(search_phrase)
    for row in search_result_answers:
        question_id = row['question_id']
        search_results2 = data_manager.get_qustion(question_id)
        if search_results2 not in search_results:
            search_results.append(search_results2)
    tags_dict = {}
    for question_id_dict in all_question_id:
        question_id = question_id_dict['id']
        tags = data_manager.join_question_with_tag(question_id)
        if tags is not None:
            tags_dict[question_id] = []
            for tag in tags:
                tags_dict[question_id].append({'tag_id': tag.pop('id'), 'name': tag.pop('name')})
    return render_template('search_results.html', user_stories=search_results, click=click_counter, tags_dict=tags_dict, search_phrase=search_phrase, answer_list=search_result_answers)


@app.route('/question/<int:question_id>/new-tag', methods=['GET'])
def add_tag(question_id):
    tag_data = {'id': ''}
    # tag_data = data_manager.get_tag(idnum)  # GET QUESTION DATA
    return render_template('add_edit_tag.html', tag_data=tag_data, question_id=question_id)


@app.route('/question/<int:question_id>/tag/<int:tag_id>/delete', methods=['GET'])
def delete_tag(tag_id, question_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect('/list')


@app.route('/handle_tag', methods=['POST', 'GET'])
def handle_tag():
    if request.method == "POST":
        # get variables from the form:
        tag_id = request.form['tag_id']
        question_id = request.form['question_id']
        name = request.form['name']
        question_tags_dict = data_manager.get_question_tags(question_id)
        all_tags_dict = data_manager.get_all_tags()

        match_in_tags = False
        for row in all_tags_dict:
            if row['name'] == name:
                match_in_tags = True

        if len(all_tags_dict) == 0: #needs to be refactored OMEGALUL
            new_tag_dict = {'name': name, 'question_id': question_id,
                            'tag_id': tag_id}  # make the dictionary without picture
            data_manager.add_tag(new_tag_dict)

        elif not match_in_tags:
                new_tag_dict = {'name': name, 'question_id': question_id,
                            'tag_id': tag_id}  # make the dictionary without picture
                data_manager.add_tag(new_tag_dict)

        else:
            tag_id = data_manager.get_tag_id(name)['id']
            for row in question_tags_dict:
                if tag_id in row.values():
                    return redirect('/')
            existing_tag_dict = {'question_id': question_id, 'tag_id': tag_id}
            print(existing_tag_dict)
            data_manager.link_tag_and_question(existing_tag_dict)

        return redirect('/')
#old version
'''        if tag_id == "":   # if no idnum => this is a new tag
            new_tag_dict = {'name': name, 'question_id': question_id, 'tag_id': tag_id}  # make the dictionary without picture
            data_manager.add_tag(new_tag_dict)
            return redirect('/')
        else:
            tag_dict = {'id': tag_id, 'name': name}
            data_manager.edit_tag(tag_dict)
'''

@app.route('/answer/<int:answer_id>/edit', methods=['POST', 'GET'])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    question_id = answer['question_id']
    question = data_manager.get_qustion(question_id)
    if request.method == 'POST':
        message = escape(request.form['answer'])
        data_manager.edit_answer_message(answer_id, message)
        # upload image start
        if request.files:
            image = request.files["image"]
            filename = data_manager.image_handler(answer['id'], 'answer', image)
            answer['image'] = filename
            data_manager.edit_answer_image(answer)
            return redirect(f'/question/{question_id}')
        # upload image end
        return redirect(f'/question/{question_id}')
    return render_template('edit-answer.html', answer_id=answer_id, question=question, answer=answer)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        hashed_password = data_manager.hash_password(password)
        user_list = data_manager.get_all_user()
        for users in user_list:
            if users['username'] == username:
                flash('Username already taken!')
                return redirect(url_for('registration'))
        else:
            data_manager.add_new_user(username, hashed_password)
        return redirect(url_for('question_list'))
    return render_template('registration.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        user_list = data_manager.get_all_user()
        for user in user_list:
            if user['username'] == username:
                hashed_password = user['password']
                user_id = user['id']
                if data_manager.verify_password(password, hashed_password):
                    session['username'] = username
                    session['user_id'] = user_id
                    return redirect(url_for('question_list'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('question_list'))


@app.route('/users')
def users():
    if 'username' not in session:
        return redirect(url_for('question_list'))
    user_list = data_manager.get_all_user()
    for user in user_list:
        user_id = user['id']
        question_counter = data_manager.count_questions(user_id)
        user['question_count'] = question_counter['count']
        answer_counter = data_manager.count_answers(user_id)
        user['answer_count'] = answer_counter['count']
        comment_counter = data_manager.count_comments(user_id)
        user['comment_count'] = comment_counter['count']
    return render_template('users.html', user_list=user_list)

@app.route('/tags')
def tags():
    tags_usage_list = data_manager.get_tags_usage()
    return render_template('tags.html', tags=tags_usage_list)

@app.route('/user/<int:user_id>')
def user_page(user_id):
    user_list = data_manager.get_all_user()
    for user in user_list:
        if user['id'] == user_id:
            user_dict = user
    question_counter = data_manager.count_questions(user_id)
    user_dict['question_count'] = question_counter['count']
    answer_counter = data_manager.count_answers(user_id)
    user_dict['answer_count'] = answer_counter['count']
    comment_counter = data_manager.count_comments(user_id)
    user_dict['comment_count'] = comment_counter['count']
    user_questions = data_manager.get_questions_for_user(user_id)
    user_answers = data_manager.get_answers_for_user(user_id)
    user_comments = data_manager.get_comments_for_user(user_id)
    return render_template('user_page.html', user_dict=user_dict, user_questions=user_questions, user_answers=user_answers, user_comments=user_comments)


@app.route('/answer/<int:answer_id>/accept', methods = ['GET', 'POST'])
def accept_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    question_id = answer['question_id']
    user_id = answer['user_id']
    if request.method == 'GET':
        data_manager.answer_accept(answer_id)
        data_manager.reputation_answer_accept(user_id)
        return redirect(f'/question/{question_id}')

@app.route('/answer/<int:answer_id>/unaccept', methods = ['GET', 'POST'])
def unaccept_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    question_id = answer['question_id']
    if request.method == 'GET':
        data_manager.answer_unaccept(answer_id)
        return redirect(f'/question/{question_id}')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
