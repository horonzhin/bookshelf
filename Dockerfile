# Используем базовый образ с поддержкой Python 3.10
FROM python:3.10

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создание и перемещение в рабочую директорию
WORKDIR /app

# Копирование зависимостей в контейнер
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Копирование остального кода
COPY . /app/

# Команда для запуска приложения
CMD python manage.py runserver 0.0.0.0:8000