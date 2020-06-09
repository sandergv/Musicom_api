FROM python:3.8-slim-buster

ADD . /api
WORKDIR /api
RUN pip install -r requirements.txt