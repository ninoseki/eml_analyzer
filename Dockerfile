# frontend
FROM node:22-alpine AS frontend

WORKDIR /usr/src/app

COPY ./frontend ./frontend

WORKDIR /usr/src/app/frontend

RUN npm install \
  && npm run build \
  &&  \rm -rf node_modules

# venv
FROM python:3.11-slim-bookworm AS venv

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libmagic-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

# main
FROM python:3.11-slim-bookworm

RUN apt-get update \
  && apt-get install -y --no-install-recommends libmagic-dev spamd \
  && apt-get clean  \
  && rm -rf /var/lib/apt/lists/*

RUN sa-update --no-gpg

WORKDIR /usr/src/app

COPY --from=frontend /usr/src/app/frontend ./frontend
COPY --from=venv /usr/src/app/.venv ./.venv

ENV PATH="/usr/src/app/.venv/bin:${PATH}"

COPY gunicorn.conf.py circus.ini ./
COPY backend ./backend

ENV SPAMD_MAX_CHILDREN=1
ENV SPAMD_PORT=7833
ENV SPAMD_RANGE="10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,127.0.0.1/32"

ENV SPAMASSASSIN_PORT=7833
ENV PORT=8000

CMD ["circusd", "/usr/src/app/circus.ini"]
