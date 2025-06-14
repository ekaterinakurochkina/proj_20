# Используем официальный slim-образ Python 3.12
# FROM python:3.12-slim
#
# # Устанавливаем рабочую директорию в контейнере
# WORKDIR /app
#
# # Устанавливаем зависимости системы
# RUN apt-get update \
#     && apt-get install -y gcc libpq-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*
#
# # Копируем файл зависимостей в контейнер
# COPY requirements.txt ./

# Используем официальный образ Nginx
FROM nginx:latest

# Копируем файл конфигурации Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем статические файлы веб-сайта в директорию для обслуживания
COPY html/ /usr/share/nginx/html/

# Открываем порт 80 для HTTP-трафика
EXPOSE 80

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# # Пробрасываем порт, который будет использовать Django
# EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]