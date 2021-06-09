FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app

ENV FLASK_APP=./app/app/server.py

RUN pip3 install -r ./app/app/requirements.txt

COPY ./app /app

CMD [ "python3" ,  FLASK_APP ]