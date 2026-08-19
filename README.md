# Task Manager API

REST API for managing tasks, categories, and users.

This project was built as a backend pet project to practice developing a FastAPI application with authentication, PostgreSQL, database migrations, automated testing, and Docker.

## Features

- User registration and authentication
- JWT-based authentication
- Password hashing with Argon2
- Role-based access control
- CRUD operations for tasks
- Task ownership
- Task categories
- PostgreSQL database
- Database migrations with Alembic
- Request and response validation with Pydantic
- Automated API tests with Pytest
- Docker and Docker Compose support

## Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL 17
- Pydantic 2
- Alembic
- PyJWT
- pwdlib / Argon2
- Pytest
- Docker
- Docker Compose
- Git

## Architecture

The application follows a layered structure:

Router
↓
Service
↓
Database / SQLAlchemy
↓
PostgreSQL

FastAPI dependency injection is used for database sessions and authentication.

## Authentication

The API uses JWT access tokens for authentication.

Authentication flow:

Register
↓
Password hashing
↓
PostgreSQL
↓
Login
↓
JWT access token
↓
Authenticated requests

Protected endpoints require a valid Bearer token:

Authorization: Bearer <access_token>

The application also supports role-based access control for protected operations.

## Database

The project uses PostgreSQL with SQLAlchemy 2.0.

Main entities:

- User
- Task
- Category

Database schema changes are managed using Alembic.

Create a migration:

alembic revision --autogenerate -m "migration message"

Apply migrations:

alembic upgrade head

Check the current migration:

alembic current

## Testing

The project includes API tests written with Pytest.

Run the test suite:

pytest

The tests cover:

- User registration
- User login
- JWT authentication
- Unauthorized requests
- Invalid input
- Task creation
- Task retrieval
- Task ownership
- Non-existent resources

## Docker

The project includes Docker configuration for running the FastAPI application together with PostgreSQL.

Build and start the containers:

docker compose up --build

The API will be available at:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs

Stop the containers:

docker compose down

PostgreSQL data is stored in a Docker named volume and persists between container restarts.

Inside Docker Compose, the application connects to PostgreSQL through the `db` service:

postgresql+psycopg2://postgres:password@db:5432/TaskManagerDB

## Environment Variables

Create a `.env` file with the required environment variables.

Example:

DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/TaskManagerDB
SECRET_KEY=your-secret-key

Do not commit real credentials or secret keys to the repository.

## Project Structure

app/
├── core/
│   ├── enums.py
│   └── security.py
│
├── database/
│   ├── database.py
│   └── models.py
│
├── routers/
│   ├── auth.py
│   ├── categories.py
│   ├── tasks.py
│   └── users.py
│
├── schemas/
│   ├── auth.py
│   ├── categories.py
│   ├── tasks.py
│   └── users.py
│
├── services/
│   ├── task_service.py
│   ├── user_service.py
│   └── ...
│
└── main.py

tests/
├── test_auth.py
└── test_tasks.py

Dockerfile
docker-compose.yml
requirements.txt
alembic.ini

## API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, open:

http://localhost:8000/docs

The Swagger UI can be used to explore and test the API endpoints.

## Project Goals

The main goal of the project was to gain practical experience with:

- REST API development
- FastAPI
- Backend application architecture
- Authentication and authorization
- PostgreSQL and relational databases
- SQLAlchemy ORM
- Database migrations
- Automated testing
- Docker and Docker Compose
- Git and GitHub