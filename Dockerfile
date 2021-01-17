FROM python:3.9-slim

MAINTAINER Chunhong Web

ENV PYTHONBUFFERED 1

COPY requirements.txt .

RUN pip install -r ./requirements.txt

WORKDIR /app

COPY ./app .
