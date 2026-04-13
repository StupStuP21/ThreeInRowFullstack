# ThreeinRow Game Fullstack

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124.2-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF)](https://vite.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Описание

Браузерная игра «Три в ряд». Приложение реализует логику и интерфейс для игры с несколькими уровнями сложности, таблицу лидеров, обработку свапов и обновлений поля, а также автоматическая маркировка проигрыша для неактивных игр.

Игра поддерживает конфигурацию уровней (простой, средний, сложный, кастомный), где предметы обозначаются буквами алфавита (с расширением как в Excel). Включает проверку на возможность хода, цепные реакции уничтожений, и Swagger-документацию для API.


## Содержание

- [Скриншоты](#скриншоты)
- [Стек технологий](#стек-технологий)
- [Структура проекта](#структура-проекта)
- [Запуск через Docker](#запуск-через-docker)
- [Локальная разработка](#локальная-разработка)
- [API](#api)
- [Игровые режимы](#игровые-режимы)
- [Лицензия](#лицензия)

## Скриншоты

<p align="center"> Страница создания игры </p>

![Alt text](/assets/create_game.png?raw=true "Страница создания игры")

<p align="center"> Страница игры </p>

![Alt text](/assets/game_field.png?raw=true "Страница создания игры")

## Стек технологий

| Слой | Технологии |
|------|-----------|
| **Frontend** | React 19, Vite 7, React Router 7, Ant Design 6, Axios |
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy 2 (async), Pydantic, APScheduler |
| **База данных** | PostgreSQL 16 |
| **Миграции** | Alembic |
| **Деплой** | Docker, Docker Compose, nginx |


## Структура проекта

```
ThreeInRowGameFullstack/
├── docker-compose.yml
├── ThreeInRowBackend/          # Бэкенд
│   ├── main.py
│   ├── config.toml             # Конфигурация БД и CORS (генерируется автоматически)
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── entrypoint.sh           # Миграции + запуск uvicorn
│   ├── alembic.ini
│   ├── migration/              # Alembic-миграции
│   └── src/
│       ├── db/                 # Модели SQLAlchemy и подключение к БД
│       ├── daos/               # Слой доступа к данным
│       ├── services/           # Бизнес-логика
│       ├── routers/            # FastAPI-роуты
│       ├── schemas/            # Pydantic-схемы
│       ├── game_logic/         # Логика игры (свапы, матчи, генерация поля)
│       └── exceptions/         # Обработка ошибок
└── ThreeInRowFrontend/         # Фронтенд
    ├── Dockerfile
    ├── nginx.conf
    ├── vite.config.js
    └── src/
        ├── app/                # Корневой компонент и роутинг
        ├── pages/              # Страницы (создание игры, игра, лидерборд)
        ├── widgets/            # Игровое поле, сайдбар
        ├── entities/           # Доменные модели (game, difficulty) + API-хуки
        ├── features/           # Фича создания игры
        └── shared/             # Общие утилиты и UI-компоненты
```


## Запуск через Docker

Единственная команда для запуска всего проекта:

```bash
docker compose up --build
```

После успешного старта:

| Сервис | Адрес |
|--------|-------|
| Фронтенд | http://localhost |
| Бэкенд API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

> Миграции применяются автоматически при старте бэкенд-контейнера.

### Остановка

```bash
docker compose down
```

Для удаления данных базы данных:

```bash
docker compose down -v
```

### Переменные окружения (docker-compose.yml)

| Переменная | Значение по умолчанию | Описание |
|---|---|---|
| `DB_NAME` | `three-row-game` | Имя базы данных |
| `DB_USER` | `postgres` | Пользователь БД |
| `DB_PASSWORD` | `user` | Пароль БД |
| `DB_HOST` | `postgres` | Хост БД (имя сервиса) |
| `FRONT_HOSTS` | `http://localhost,...` | Разрешённые CORS-хосты |
| `VITE_API_URL` | `http://localhost:8000` | URL бэкенда для фронтенда (build arg) |


## Локальная разработка

### Требования

- Python 3.11+
- Node.js 20+
- PostgreSQL 16

### Бэкенд

```bash
cd ThreeInRowBackend

# Создать и активировать виртуальное окружение
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# Установить зависимости
pip install -r requirements.txt

# Применить миграции (config.toml генерируется автоматически при первом запуске)
alembic upgrade head

# Запустить сервер
uvicorn main:app --reload
```

Бэкенд доступен на `http://localhost:8000`.

Конфигурация хранится в `config.toml` (создаётся автоматически):

```toml
[db_connection]
db_name = "three-row-game"
db_user = "postgres"
db_password = "user"
db_host = "localhost"
db_port = 5432

[front_connection]
hosts = ["http://localhost:5173", "http://127.0.0.1:5173"]
```

### Фронтенд

```bash
cd ThreeInRowFrontend
npm install
npm run dev
```

Фронтенд доступен на `http://localhost:5173`.

По умолчанию обращается к бэкенду на `http://127.0.0.1:8000`. Чтобы изменить адрес, создайте файл `.env`:

```env
VITE_API_URL=http://localhost:8000
```


## API

Полная документация доступна в **Swagger UI** по адресу `http://localhost:8000/docs`.

### Основные эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/difficulties` | Список уровней сложности |
| `GET` | `/difficulties/{id}` | Уровень сложности по ID |
| `POST` | `/create_game/create` | Создать новую игру |
| `GET` | `/game/{id}` | Состояние игры |
| `GET` | `/game/{id}/score` | Текущий счёт |
| `POST` | `/game/{id}/swap` | Сделать свап элемента |
| `POST` | `/game/{id}/refresh` | Полностью обновить поле (со штрафом) |
| `PATCH` | `/game/{id}` | Обновить поля игры (например, сдаться) |
| `GET` | `/leaderboard/{difficulty_id}` | Топ-10 результатов по сложности |


## Игровые режимы

### Уровни сложности

| Уровень | Поле | Цель | Особенности |
|---------|------|------|-------------|
| **Простой** | 12×12 | 40 очков | — |
| **Средний** | 8×8 | 50 очков | Одним свапом |
| **Сложный** | 8×8 | 25 очков | Одним свапом + случайный предмет |
| **Кастомный** | любое | любая | Все параметры задаются вручную |

### Механики

- **Цепные реакции** — после уничтожения совпадений новые элементы падают сверху и могут образовывать новые матчи автоматически.
- **Автообновление поля** — если на поле не осталось возможных ходов, поле перегенерируется без штрафа.
- **Таймаут** — игра автоматически засчитывается как поражение при бездействии более 2 часов.
- **Режим одним свапом** — каждый свап должен приводить к уничтожению элементов, иначе свап отменяется.
- **Режим случайного предмета** — очки засчитываются только за совпадения конкретного случайного элемента.
- **Таблица лидеров** — топ-10 завершённых игр по каждому уровню, отсортированные по времени.


## Лицензия

Этот проект лицензирован под MIT License — см. файл [LICENSE](ThreeInRowBackend/LICENSE) для деталей.


