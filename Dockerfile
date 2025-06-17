FROM python:3.12-slim

WORKDIR /usr/src/app

COPY . . 

RUN pip install --default-timeout=100 -r requirements.txt
