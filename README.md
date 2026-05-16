# API Organizational Structure

REST API для управления организационной структурой компании.  
Поддерживает дерево подразделений и управление сотрудниками.

## Стек

- **FastAPI** — веб-фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **Docker + docker-compose** — контейнеризация
- **pytest** — тесты

## Структура проекта
app/
├── models/ # SQLAlchemy модели
├── schemas/ # Pydantic схемы
├── repositories/ # Слой работы с БД
├── services/ # Бизнес-логика
├── routers/ # FastAPI роутеры
├── database.py # Подключение к БД
├── config.py # Настройки
├── exceptions.py # HTTP исключения
└── main.py # Точка входа
alembic/ # Миграции
tests/ # Тесты

## Запуск

### 1. Клонируй репозиторий

```bash
git clone https://github.com/yaroslav-grishanov98/API_Organizational_Structure.git
cd API_Organizational_Structure
```

### 2. Запусти через docker-compose
```bash
docker-compose up --build
```

### 3. Примени миграции
```bash
docker-compose exec app alembic upgrade head
```

### 4. Готово!
API доступно по адресу: http://localhost:8000
Документация (Swagger): http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc


### 5. Запуск тестов
```bash
docker-compose exec app pytest tests/ -v
```