# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry==2.2.1


# Создаём рабочую директорию
WORKDIR /app

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости без dev
RUN poetry config virtualenvs.create false \
    && poetry install --no-root



# Копируем весь исходный код
COPY . .

# Указываем команду запуска gRPC сервера
CMD ["python", "-m", "app.auth.gRPC.auth_server"]
