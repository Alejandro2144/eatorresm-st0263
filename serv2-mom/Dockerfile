FROM python:3.9-slim as dev
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3-pip libpq-dev

COPY . .
RUN pip install -r requirements.txt

ENV APP_DIR=/app
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}