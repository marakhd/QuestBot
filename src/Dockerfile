# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем curl и venv для poetry
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.7.0

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости с poetry
RUN poetry install --no-root --only main

# Копируем остальные файлы в контейнер
COPY . .

# Указываем команду для запуска бота
CMD ["poetry", "run", "python", "main.py"]
