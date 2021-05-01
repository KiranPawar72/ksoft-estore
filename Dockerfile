FROM python:latest

MAINTAINER kiran@mystore.com

RUN mkdir /automation

COPY ./sqaapitest /automation/sqaapitest
COPY ./setup.py /automation

WORKDIR /automation
RUN python3 setup.py install
