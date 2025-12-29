# Используем Python на базе Debian Bookworm (стабильнее для РФ)
FROM python:3.12-slim

# Системные зависимости с российским зеркалом
RUN find /etc/apt/sources.list.d/ -type f -name "*.sources" -exec sed -i \
    -e 's|http://deb.debian.org/debian|https://mirror.yandex.ru/debian|g' \
    -e 's|http://security.debian.org/debian-security|https://mirror.yandex.ru/debian-security|g' {} \; && \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential libpq-dev curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install --no-cache-dir poetry==2.2.1

# Зеркало PyPI (Яндекс — самое быстрое и стабильное)
ENV POETRY_PYPI_MIRROR_URL=https://mirror.yandex.ru/mirrors/pypi/simple/

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Копируем код
COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app/proto"

CMD ["poetry", "run", "python", "app/main.py"]