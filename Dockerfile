FROM python:3.12
#set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /app

COPY . /app
WORKDIR /app

# install chrome binary and specific chromedriver version for selenium
RUN apt-get update \
    && apt-get install -y \
        chromium \
        wget \
        unzip \
    && wget https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.68/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip chromedriver-linux64 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


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

CMD ["gunicorn", "receipt_scraper_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "3", "--timeout", "3600", "--log-level=debug"]
# RUN gunicorn receipt_scraper_project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 3 --timeout 3600 --log-level=debug