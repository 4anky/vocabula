FROM python:3.13-slim AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir poetry \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev --no-root

FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd -g 1000 group && \
    useradd -u 1000 -g group user

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY ./vocabula ./vocabula

USER user

CMD ["uvicorn", "vocabula.main:app", "--host", "0.0.0.0", "--port", "8000"]
