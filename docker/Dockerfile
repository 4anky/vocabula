FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd -g 1000 group && \
    useradd -u 1000 -g group user

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev --no-root

COPY ./vocabula/ ./vocabula

CMD ["uvicorn", "vocabula.main:app", "--host", "0.0.0.0", "--port", "8000"]
