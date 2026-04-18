FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY raspberry_service/app/ .
RUN pip install --no-cache-dir redis kafka-python fastapi uvicorn python-multipart


# Запуск приложения
CMD ["python", "rustberi_service.py"]