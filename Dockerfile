FROM python:3
ENV PYTHONUNBUFFERED=1

ARG code_location
RUN mkdir /code
WORKDIR /code

COPY . /code/
WORKDIR /code/$code_location

RUN pip install pip
RUN pip install pipenv
RUN pipenv install --dev --system --ignore-pipfile