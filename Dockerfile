FROM python:3.11-slim

WORKDIR /app

COPY Bot/requirements/prod.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "-m", "Bot.main"]