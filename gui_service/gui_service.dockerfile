FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
# Установка зависимостей
COPY gui_service/app/ .
RUN pip install --no-cache-dir redis fastapi uvicorn python-multipart

# Запуск приложения
CMD ["python", "gui_service.py"]