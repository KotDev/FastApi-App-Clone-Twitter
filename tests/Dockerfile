FROM python:3.10

ENV PYTHONUNBUFFERED=1

LABEL authors="danil"

WORKDIR /test


COPY poetry.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install

COPY . /test

CMD ["sh", "-c", "pytest --maxfail=1 --disable-warnings -q"]