FROM python:3

LABEL maintainer="istpdeveloper"

ENV PYTHONUNBUFFERED 1
RUN python -m venv venv
RUN . ./venv/bin/activate
RUN pip freeze > requirements.txt
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /web
WORKDIR /web
COPY . .
# wait-for-it.sh
COPY wait-for-it.sh ./
RUN chmod +x wait-for-it.sh