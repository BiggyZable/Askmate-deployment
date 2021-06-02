import csv
import os

QUESTION_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTION_IMAGE_UPLOADS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'static/uploads/questions_images'
ANSWER_IMAGE_UPLOADS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'static/uploads/answers_images'

QUESTION_HEADER = ['id','submission_time','view_number','vote_number','title','message','image']
ANSWER_HEADER = ['id','submission_time','vote_number','question_id','message','image']


def read_from_question():
    lst = []
    with open(QUESTION_PATH, 'rt', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lst.append(row)
    return lst


def read_from_answer():
    lst = []
    with open(ANSWER_PATH, 'rt', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lst.append(row)
    return lst


def write_question_to_file(questions):
    with open(QUESTION_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=QUESTION_HEADER)
        writer.writeheader()
        for row in questions:
            writer.writerow(row)


def write_answer_to_file(answer_list):
    with open(ANSWER_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ANSWER_HEADER)
        writer.writeheader()
        for row in answer_list:
            writer.writerow(row)


def upload_image(image, question_or_answer, filename):
    image_folder = QUESTION_IMAGE_UPLOADS if question_or_answer == 'question' else ANSWER_IMAGE_UPLOADS
    file_path = os.path.join(image_folder, filename)
    image.save(file_path)
    print(file_path)
    print('test', image)
    print("Image saved")    # OK MESSAGE
    return str(file_path)


def delete_image(file_path):
    try:
        os.remove(file_path)
        print(f'{file_path} image is deleted.')
    except:
        pass

