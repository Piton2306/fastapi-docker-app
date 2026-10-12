# ==========================================
# ЭТАП 1: Builder (Сборка зависимостей)
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Устанавливаем системные зависимости для сборки (если потребуются C-библиотеки)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем список зависимостей и собираем wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# ЭТАП 2: Final Runtime (Минимальный боевой образ)
# ==========================================
FROM python:3.12-slim AS runner

WORKDIR /app

# Создаем непривилегированного системного пользователя appuser (UID 10001)
# Запуск от root в контейнерах КАТЕГОРИЧЕСКИ ЗАПРЕЩЕН в проде!
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

# Копируем только готовые установленные пакеты из этапа builder
COPY --from=builder /root/.local /home/appuser/.local

# Копируем исходный код приложения и отдаем права владельца appuser
COPY --chown=appuser:appgroup main.py .

# Добавляем установленные пакеты в системный PATH пользователя appuser
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Переключаемся на non-root пользователя
USER 10001

# Декларируем открываемый порт
EXPOSE 8000

# Запуск ASGI-сервера Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]