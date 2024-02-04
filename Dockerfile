# Frontend
FROM node:20-alpine3.18 as frontend

WORKDIR /usr/src/app

COPY ./frontend ./frontend

WORKDIR /usr/src/app/frontend

RUN npm install && npm run build && rm -rf node_modules

# Backend
FROM python:3.11-slim-bookworm as backend

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libmagic-dev  \
  && apt-get clean  \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --without dev

# Main
FROM python:3.11-slim-bookworm

COPY --from=backend /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=backend /usr/local/bin/ /usr/local/bin/

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libmagic-dev spamd \
  && apt-get clean  \
  && rm -rf /var/lib/apt/lists/*

RUN sa-update --no-gpg

WORKDIR /usr/src/app

COPY gunicorn.conf.py circus.ini ./
COPY backend ./backend
COPY --from=frontend /usr/src/app/frontend ./frontend

ENV SPAMD_MAX_CHILDREN=1
ENV SPAMD_PORT=7833
ENV SPAMD_RANGE="10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,127.0.0.1/32"

ENV SPAMASSASSIN_PORT=7833

ENV PORT=8000

CMD ["circusd", "/usr/src/app/circus.ini"]
