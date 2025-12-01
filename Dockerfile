# Dockerfile for Burt's Books
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=burts_books.settings

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

RUN mkdir -p /app/media /app/staticfiles

RUN python deploy_init.py

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "burts_books.wsgi:application"]
