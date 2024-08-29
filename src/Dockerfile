FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY ./alembic.ini .

COPY ./migrations .

COPY ./src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

RUN pip install alembic

CMD ["sh", "-c", "alembic -c /app/src/alembic.iniupgrade head && uvicorn src.main:app"]

