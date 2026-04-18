FROM python:3.11-slim

WORKDIR /app

COPY rustberi_emulator/app/requests_emulator.py .

RUN pip install requests

CMD ["python", "requests_emulator.py"]