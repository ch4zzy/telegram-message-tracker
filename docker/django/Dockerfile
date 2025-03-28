FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic

# Expose the port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
