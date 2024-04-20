ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-bullseye as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ENV POETRY_VERSION=1.7.1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-ansi --no-root;


FROM python:${PYTHON_VERSION}-bullseye as runner

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=base ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY core ./app/core
COPY server.py ./app/server.py
COPY gunicorn.conf.py ./app/gunicorn.conf.py
COPY entrypoint.sh ./app/entrypoint.sh
COPY alembic.ini ./app/alembic.ini
COPY alembic ./app/alembic
COPY pytest.ini ./app/pytest.ini
COPY migrate-db.sh ./app/migrate-db.sh
COPY downgrade-db.sh ./app/downgrade-db.sh

WORKDIR /app

RUN chmod +x entrypoint.sh
RUN chmod +x migrate-db.sh
RUN chmod +x downgrade-db.sh

EXPOSE 8000

CMD ./entrypoint.sh
