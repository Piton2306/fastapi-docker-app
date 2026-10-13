import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

app = FastAPI(title="Production DevOps Service")

# Считываем параметры подключения из переменных окружения (12-Factor App)
DB_HOST = os.getenv("DB_HOST", "192.168.1.160")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "production_db")
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Инициализируем пул соединений к СУБД
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@app.get("/")
def health_check():
    """Эндпоинт проверки жизнеспособности сервиса (Health Check)"""
    return {"status": "ok", "service": "fastapi-backend", "version": "1.0.0"}

@app.get("/users")
def get_users():
    """Эндпоинт получения пользователей из реальной БД"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT id, username, email FROM users;"))
            users = [{"id": row[0], "username": row[1], "email": row[2]} for row in result]
            return {"total": len(users), "users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")