# dX0k_tech_task
Сервис управления заказами, техническое задание на позицию "Python Backend Developer". Текст задания доступен [прямо в репозитории](https://github.com/SLotAbr/dX0k_tech_task/blob/main/Backend%20Python%20Task.pdf).

## Детали

Безопасность: 
* JWT аутентификация (OAuth2 Password Flow)
* Ограничение кросс-доменных запросов на основе CORS Middleware
* Rate Limiting Middleware на основе плавной версии алгоритма "the sliding window"
* Защита от SQL инъекций

Компоненты: 
* Очереди сообщений на RabbitMQ
* Фоновая обработка задач на Celery
* Кэширование ответов на Redis
* Миграции на Alembic
* Docker для инфраструктуры
* Ядро на FastAPI, Pytest тесты, все взаимодействия асинхронны

## Инструкции по установке и запуску
1. Виртуальное окружение, его активация: `python3.11 -m venv venv`, `source venv/bin/activate`
1. Установка зависимостей: `python -m pip install -r requirements.txt`
1. Вся инфраструктура находится в Docker контейнерах. Для сборки и запуска: `docker compose up -d`
1. Миграции: `make migrate`
1. Приложение опирается на Celery для выполнения фоновых задач. Скрипт для запуска: `make celery-worker`
1. Осталось только запустить сам сервер: `make up`

Swagger UI документация с описанием всех методов приложения доступна локально: `http://localhost:8000/docs`
