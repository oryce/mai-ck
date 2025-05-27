FROM python:3.11.9-slim-bullseye

WORKDIR /app

COPY . .

ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    tesseract-ocr-rus \
    tesseract-ocr-eng 
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
