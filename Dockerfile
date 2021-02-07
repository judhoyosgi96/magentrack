FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN apt-get -y update 
RUN apt-get install -y libgdal-dev

RUN python -m pip install -r requirements.txt

COPY . /code/

