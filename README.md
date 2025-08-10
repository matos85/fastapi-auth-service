# 🔐 FastAPI Authentication Service

Микросервис аутентификации и управления пользователями на основе FastAPI с JWT токенами.  
Простая в развертывании система для защиты ваших приложений.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## 🌟 Особенности

- Регистрация и аутентификация пользователей
- JWT токены для защиты API
- Полное управление учетными записями
- Автоматическая генерация документации (Swagger/ReDoc)
- Готовые Docker-образы для быстрого развертывания
- Миграции баз данных через Alembic

## ⚙️ Технологии

- **Backend**: Python 3.12, FastAPI
- **База данных**: PostgreSQL
- **Аутентификация**: JWT (HS256)
- **Хеширование**: Bcrypt
- **Оркестрация**: Docker Compose
- **Миграции**: Alembic

## 🚀 Быстрый старт

### Требования
- Docker 20.10+
- Docker Compose 1.29+

### Запуск за 3 шага:
```bash
# 1. Клонировать репозиторий
git clone https://github.com/<your-username>/fastapi-auth-service.git
cd fastapi-auth-service

# 2. Запустить сервисы
docker-compose up --build -d

# 3. Проверить работу
curl http://localhost:8000
# Ответ: {"status":"ok","version":"1.0.0"}
