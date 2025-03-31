# base structure for celery worker

FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt
