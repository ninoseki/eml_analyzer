# build env
FROM node:14-alpine as build

COPY ./frontend /frontend
WORKDIR /frontend
RUN npm install && npm run build && rm -rf node_modules

# prod env
FROM python:3.8-slim-buster

RUN apt-get update \
  && apt-get install -y spamassassin supervisor libmagic-dev  \
  && apt-get clean  \
  && rm -rf /var/lib/apt/lists/*

RUN sa-update

WORKDIR /backend

COPY pyproject.toml /backend
COPY poetry.lock /backend
COPY app /backend/app
COPY --from=build /frontend /backend/frontend

RUN pip3 install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY supervisord.conf /etc/supervisord.conf

# spamd envs
ENV SPAMD_MAX_CHILDREN=1 \
  SPAMD_PORT=7833 \
  SPAMD_RANGE="10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,127.0.0.1/32"

# app envs
ENV SPAMASSASSIN_PORT=7833 \
  PORT=8000

EXPOSE $PORT

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
