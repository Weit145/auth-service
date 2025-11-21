# Используем официальный Python
FROM python:3.12-slim

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install --no-cache-dir poetry==2.2.1

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Копируем весь код
COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app/proto"


CMD ["poetry", "run", "python", "app/main.py"]
