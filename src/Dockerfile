FROM python:3.10

ENV PYTHONUNBUFFERED=1

LABEL authors="danil"

WORKDIR app

COPY . /app

COPY poetry.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install

CMD ["poetry", "run", "python", "app.py"]
