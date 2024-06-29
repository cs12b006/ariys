FROM python:3.10.13-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV ENV="dev"
ENV SERVICE_NAME="ariys"

RUN apt-get update -y \
    && apt-get -y install --fix-missing curl postgresql postgresql-contrib postgresql-client iproute2 nginx \
    && apt-get clean

COPY ariys/requirements.txt /code/ariys/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /code/ariys/requirements.txt

#COPY ariys/nginx.conf /etc/nginx/sites-enabled/default

COPY ariys /code/ariys
COPY ./.flake8 ./pyproject.toml /code/

WORKDIR /code/
RUN mkdir -p /code/ariys/staticfiles

