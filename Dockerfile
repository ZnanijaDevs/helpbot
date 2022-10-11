FROM python:3.10.0-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get install -y --no-install-recommends git

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port $PORT