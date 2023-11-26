# build env
FROM node:20-alpine3.18 as build

WORKDIR /usr/src/app

COPY frontend ./frontend

WORKDIR /usr/src/app/frontend

ENV NODE_OPTIONS --openssl-legacy-provider
RUN npm install && npm run build && rm -rf node_modules

# prod env
FROM python:3.11-slim-bookworm

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential spamassassin libmagic-dev  \
  && apt-get clean  \
  && rm -rf /var/lib/apt/lists/*

RUN sa-update

WORKDIR /usr/src/app

COPY requirements.txt pyproject.toml poetry.lock gunicorn.conf.py ./
COPY backend ./backend
COPY --from=build /usr/src/app/frontend ./frontend

RUN pip install --no-cache-dir -r requirements.txt \
  && poetry install --without dev

COPY circus.ini /etc/circus.ini

ENV SPAMD_MAX_CHILDREN=1
ENV SPAMD_PORT=7833
ENV SPAMD_RANGE="10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,127.0.0.1/32"
ENV SPAMASSASSIN_PORT=7833

ENV PORT=8000
EXPOSE $PORT

CMD ["poetry", "run", "circusd", "/etc/circus.ini"]
