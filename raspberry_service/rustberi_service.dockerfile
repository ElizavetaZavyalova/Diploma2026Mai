FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
# Установка зависимостей
COPY raspberry_service/app/ .
RUN pip install --no-cache-dir redis kafka-python fastapi uvicorn python-multipart


# Запуск приложения задержка так как kafka не успевает прочухаться
CMD ["python", "rustberi_service.py"]