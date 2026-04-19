## Двухсервисная система LLM-консультаций

Система состоит из двух логически и технически независимых сервисов:
 **Auth Service** — регистрация, логин, выдача JWT
- **Bot Service** — Telegram-бот с LLM-консультациями через OpenRouter
 каждый из которых выполняет строго определённую роль. Архитектура построена по принципу разделения ответственности: один сервис отвечает исключительно за аутентификацию и выпуск токенов, второй — за предоставление функциональности LLM-консультаций через Telegram-бота. Такое разделение позволяет изолировать чувствительную логику работы с пользователями и учетными данными от прикладного сервиса, работающего с внешними пользователями и внешними API.
Ключевая идея проекта заключается в том, что Telegram-бот не знает ничего о пользователях, паролях и механизмах регистрации. Он доверяет только корректно подписанному и не истёкшему JWT-токену, выданному специализированным сервисом авторизации. Это приближает архитектуру проекта к реальным микросервисным системам и демонстрирует принципы построения безопасных распределённых приложений.

## Требования

- Python 3.11+
- Docker (RabbitMQ + Redis)
- Telegram Bot Token
- OpenRouter API Key

## Установка и запуск

### Auth Service

cd auth_service
pip install uv
uv venv
.venv\Scripts\activate
uv pip install -r pyproject.toml
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


### Bot Service
cd bot_service
uv venv
.venv\Scripts\activate
uv pip install -r pyproject.toml

### RabbitMQ и Redis
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
docker run -d --name redis -p 6379:6379 redis:7

### Celery
cd bot_service
celery -A app.infra.celery_app worker --loglevel=info -P solo

### Telegram bot

cd bot_service
python -m app.main

## Cценарий работы

1.Зарегистрируйся в Auth Service через Swagger: http://localhost:8000/docs
2.Получи токен через POST /auth/login
3.Отправь токен боту командой /token <token>
4.Отправь любой вопрос — бот передаст его и вернёт ответ LLM


## Скрины
## Скриншоты

### Регистрация (POST /auth/register)
![Register](screen/registration.png)

### Логин (POST /auth/login)
![Login](screen/login.png)

### Профиль (GET /auth/me)
![Me](screen/auth_me.png)

### Telegram бот
![Telegram](screen/telegram.png)

### RabbitMQ очереди
![RabbitMQ](screen/rabbitmq.png)

### Celery worker
![Celery](screen/celery.png)

### Тесты
![Tests](screen/tests.png)


## Тестирование

### Auth Service
cd auth_service
pytest tests/ -v

### Bot Service
cd bot_service
pytest tests/ -v


