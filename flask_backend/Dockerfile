# Dockerfile
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]

