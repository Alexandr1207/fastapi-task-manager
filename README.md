# FastAPI Task Manager

REST API для управления задачами с аутентификацией пользователей, категориями и разграничением доступа. Сделан как pet-проект для отработки слоистой архитектуры (Router → Service → DB) в FastAPI.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

## Возможности

- Регистрация и аутентификация пользователей через JWT
- Хэширование паролей (Argon2)
- CRUD для задач (tasks) с приоритетом, статусом и дедлайном
- Категории задач с уникальными именами
- Разграничение доступа: пользователь видит и редактирует только свои задачи
- Валидация данных на уровне Pydantic-схем
- Миграции схемы БД через Alembic

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **PostgreSQL** — база данных
- **Alembic** — миграции
- **Pytest** — тесты
- **Docker / Docker Compose** — контейнеризация

## Архитектура

Проект построен по слоистому принципу:

```
Router (обработка HTTP-запросов, валидация входных данных)
   ↓
Service (бизнes-логика)
   ↓
Database (SQLAlchemy-модели, запросы к БД)
```

Это разделение сделано осознанно: роутер не знает деталей работы с БД, сервисный слой не зависит от FastAPI — такую структуру проще тестировать и расширять.

## Скриншоты

> Task endpoints
> ![img.png](screenshots/img.png)
> Categories endpoints
> ![img_1.png](screenshots/img_1.png)
> User and auth endpoints
> ![img_2.png](screenshots/img_2.png)
> Successfull authorization
> ![img_3.png](screenshots/img_3.png)
> 
> Get title endpoint result
> ![img_4.png](screenshots/img_4.png)
> User role error
> ![img_5.png](screenshots/img_5.png)
> ER-diagram
> ![img_6.png](screenshots/img_6.png)

## Быстрый старт

Проект поднимается одной командой через Docker Compose — не нужно вручную ставить PostgreSQL или настраивать окружение.

```bash
git clone https://github.com/Alexandr1207/fastapi-task-manager.git
cd fastapi-task-manager

cp .env.example .env
# при необходимости поправь значения в .env

docker-compose up --build
```

После запуска:
- API доступно на `http://localhost:8000`
- Интерактивная документация (Swagger UI) — `http://localhost:8000/docs`

Миграции применяются автоматически при старте контейнера. Если нужно прогнать их вручную:

```bash
docker-compose exec app alembic upgrade head
```

## Примеры запросов

**Регистрация пользователя**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "SecurePass123"}'
```

**Логин и получение токена**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'
```

**Создание задачи (нужен Bearer-токен)**
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer <твой_токен>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Первая задача", "priority": "high", "deadline": "2026-12-31"}'
```

## Тесты

```bash
docker-compose exec app pytest
```

Покрыты: регистрация/логин, обработка невалидных данных, доступ к чужим/несуществующим ресурсам.

## Возможные улучшения

- [ ] Пагинация для списка задач
- [ ] Фильтрация задач по статусу/приоритету/категории
- [ ] Rate limiting на auth-эндпоинтах
- [ ] Логирование в структурированном формате

## Автор

Alexandr — [GitHub](https://github.com/Alexandr1207)