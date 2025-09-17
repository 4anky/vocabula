FROM python:3.13-slim

RUN groupadd -g 1000 group && \
    useradd -u 1000 -g group user

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# копируем сначала только зависимости, чтобы кешировать pip install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# затем весь код
COPY . /app

# Команда запуска FastAPI
CMD ["uvicorn", "vocabula.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
