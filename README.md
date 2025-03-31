# Сервис для обработки событий от датчиков

## Разработка
 - Требуется python >= 3.11
 - Устанавливаем poetry: `pip install poetry`
 - Устанавливаем зависимости: `poetry install`
 - Установить линтеры `pre-commit install`

## Локльный запуск
 - Перед запуском приложения запуск бд в docker: 
 ```docker run --name event_handler_db -p 5432:5432 -e POSTGRES_USER=event_handler -e POSTGRES_PASSWORD=111111 -e POSTGRES_DB=event_handler_db -d -v "/absolute/path/to/directory-with-init-scripts":/docker-entrypoint-initdb.d postgres:16```
 - После установки зависимостей и запуска бд - запуск сервиса: `fastapi dev app/main.py`
 - После запуска сервиса локально доку по api можно найти тут: `http://127.0.0.1:8000/docs#/`

## Тесты
 - Запуск тестов: команда `pytest` 