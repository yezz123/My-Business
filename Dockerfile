# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /MyBusiness
COPY requirements.txt ./MyBusiness
RUN pip install -r requirements.txt
COPY . /MyBusiness/