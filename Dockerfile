FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt
