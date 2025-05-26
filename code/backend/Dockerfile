FROM python:3.11.9-slim-bullseye

WORKDIR /app

COPY . .

ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache tesseract-ocr
RUN apk add --no-cache poppler-utils
RUN pip install --no-cache-dir -r requirements.txt
RUN apk add tesseract-ocr-data-rus
RUN apk add tesseract-ocr-data-eng
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
