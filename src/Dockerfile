# Используем официальное минимальное изображение Python
FROM python:3.12-slim

# Устанавливаем необходимые системные пакеты
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED 1

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app

# Копируем весь исходный код в контейнер
COPY . /app/

# Устанавливаем сокеты (если они понадобятся для работы)
COPY . /app/
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

