# Department API

REST API для управления отделами и сотрудниками.

## Репозиторий

```bash
git@github.com:REBIZ1/Departments.git
```

## Запуск проекта

1. Клонировать репозиторий:

```bash
git clone git@github.com:REBIZ1/Departments.git
```

2. Создать файл `.env`:

```.env
MODE="LOCAL"

DB_USER=test1
DB_PASS=test1
DB_HOST=department_db
DB_PORT=5432
DB_NAME=department
```

3. Запустить проект:

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```bash
http://localhost:7777
```

Swagger документация:

```bash
http://localhost:7777/docs
```

## Используемые технологии

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Docker Compose
