# Frontend
FROM node:20-alpine3.18 as frontend

WORKDIR /usr/src/app

COPY ./frontend ./frontend

WORKDIR /usr/src/app/frontend

RUN npm install && npm run build && rm -rf node_modules

# Backend
FROM python:3.11-slim-bookworm as backend

RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential libmagic-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
	&& poetry install --without dev

# Main
FROM python:3.11-slim-bookworm

COPY --from=backend /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=backend /usr/local/bin/ /usr/local/bin/

RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential libmagic-dev \
	&& apt-get clean  \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

ARG USERNAME=nobody

USER $USERNAME

COPY --chown=$USERNAME gunicorn.conf.py ./
COPY --chown=$USERNAME backend ./backend
COPY --chown=$USERNAME --from=frontend /usr/src/app/frontend ./frontend

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "backend.main:app"]
