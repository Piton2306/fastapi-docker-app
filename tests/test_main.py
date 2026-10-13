import pytest
from fastapi.testclient import TestClient
from main import app

# Создаем тестового виртуального клиента (без запуска реального веб-сервера)
client = TestClient(app)

def test_health_check():
    """Тест 1: Проверяем, что эндпоинт / отдает 200 OK и статус ok"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "fastapi-backend"
