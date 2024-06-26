FROM python:3.11-slim

RUN mkdir /backend_app

WORKDIR /backend_app

RUN pip install -U pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
