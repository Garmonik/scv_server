FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/proj/req.txt
COPY service /service
WORKDIR /service

EXPOSE 8000

RUN pip install -r /app/proj/req.txt

RUN adduser --disabled-password test-user
USER test-user