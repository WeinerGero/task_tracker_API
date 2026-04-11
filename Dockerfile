FROM python:3.12-slim

# Запрещаем Python писать .pyc файлы на диск
ENV PYTHONDONTWRITEBYTECODE=1
# Запрещаем буферизацию вывода (логи будут видны сразу)
ENV PYTHONUNBUFFERED=1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Запускаем приложение от не-root пользователя
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Порт, который слушает приложение
EXPOSE 8000