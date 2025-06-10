FROM python:3.12
#set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /app



COPY . /app
WORKDIR /app

# install chrome binary for selenium
RUN apt-get update \
    && apt-get install -y \
        chromium-browser \
        chromium-chromedriver 


# apt-get update \
#     && apt-get install -y \
#         libpq-dev \
#         gcc \
#         curl \
#         libxml2-dev \
#         libxslt-dev \
#         libffi-dev \
#         libcairo2-dev \
#         libpango1.0-dev \
#     && apt-get clean \
#     && 

RUN pip3 install --upgrade pip \
    && pip3 install gunicorn \
    && pip3 install psycopg2 \
    && pip3 install -r requirements.txt 