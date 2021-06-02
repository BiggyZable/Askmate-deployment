FROM python:3.9.5-slim
WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

EXPOSE 5000
ENV FLASK_APP=./app/server.py

ADD . /app
RUN pip3 install -r ./app/requirements.txt
ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]
