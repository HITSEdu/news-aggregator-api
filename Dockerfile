FROM python:3.10
# python slim
WORKDIR /usr/src/app

COPY . . 

RUN pip install -r requirements.txt
