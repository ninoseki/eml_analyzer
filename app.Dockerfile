# frontend
FROM node:24-alpine AS frontend

WORKDIR /usr/src/app

COPY ./frontend ./frontend

WORKDIR /usr/src/app/frontend

RUN npm install \
	&& npm run build \
	&&  \rm -rf node_modules

# venv
FROM python:3.12-slim-bookworm AS venv

RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential git libmagic-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

# main
FROM python:3.12-slim-bookworm

RUN apt-get update \
	&& apt-get install -y --no-install-recommends libmagic-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

ARG USERNAME=nobody

USER $USERNAME

WORKDIR /usr/src/app

COPY --chown=$USERNAME --from=frontend /usr/src/app/frontend ./frontend
COPY --chown=$USERNAME --from=venv /usr/src/app/.venv ./.venv

ENV PATH="/usr/src/app/.venv/bin:${PATH}"

COPY --chown=$USERNAME gunicorn.conf.py ./
COPY --chown=$USERNAME backend ./backend

CMD ["gunicorn", "-k", "uvicorn_worker.UvicornWorker", "backend.main:app"]
