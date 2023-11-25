# build env
FROM node:20-alpine3.18 as build

WORKDIR /usr/src/app

COPY ./frontend ./frontend

WORKDIR /usr/src/app/frontend

ENV NODE_OPTIONS --openssl-legacy-provider
RUN npm install && npm run build && rm -rf node_modules

# prod env
FROM python:3.11-slim-bookworm

RUN apt-get update \
	&& apt-get install -y --no-install-recommends libmagic-dev  \
	&& apt-get clean  \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt pyproject.toml poetry.lock gunicorn.conf.py ./
COPY backend ./backend
COPY --from=build /frontend ./frontend

RUN pip install --no-cache-dir -r requirements.txt \
	&& poetry install --without dev

ENV PORT 8000
EXPOSE $PORT

CMD peotry run gunicorn -k uvicorn.workers.UvicornWorker backend.main:app
