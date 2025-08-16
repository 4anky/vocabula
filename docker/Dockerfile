FROM python:3.13-slim

# Установим зависимости для Poetry
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Устанавливаем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Копируем весь проект
COPY . .

# Устанавливаем зависимости без виртуального окружения
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only production

# Открываем порт
EXPOSE 8000

# Команда запуска FastAPI
CMD ["poetry", "run", "uvicorn", "vocabula.main:app", "--host", "0.0.0.0", "--port", "8000"]
