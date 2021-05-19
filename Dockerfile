FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano gcc libc-dev g++ libffi-dev

ARG code_location
RUN mkdir /code
WORKDIR /code

COPY . /code/
WORKDIR /code/$code_location

RUN pip install --upgrade pip
RUN pip install -r requirements.txt