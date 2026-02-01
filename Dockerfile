FROM python:3.13-alpine as base

WORKDIR /app


RUN pip install --no-cache-dir poetry==2.1.3 && \
    poetry config virtualenvs.create false 

COPY poetry.lock pyproject.toml ./

EXPOSE 5001

# ------- DEV -------

FROM base AS dev
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

# ------- PROD -------
FROM base AS prod
RUN poetry install --no-interaction --no-ansi --no-root --no-dev

COPY . .
CMD ["flask", "run"]
