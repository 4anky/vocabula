FROM python:3.13-slim

WORKDIR /vocabula

COPY requirements/prod.txt .
RUN pip3 install -r prod.txt

COPY ../vocabula .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
