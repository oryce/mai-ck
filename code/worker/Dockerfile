FROM python:3.13-slim-bullseye

WORKDIR /app

COPY . .

ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-rus \
    poppler-utils

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "-m", "app.main"]