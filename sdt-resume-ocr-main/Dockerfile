FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y poppler-utils

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY .env .env
COPY src/ src/

CMD [ "python", "-m", "src.main" ]