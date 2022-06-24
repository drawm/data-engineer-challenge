FROM python:3.7.1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./ /app

COPY wait-for-it.sh /app/wait-for-it.sh
