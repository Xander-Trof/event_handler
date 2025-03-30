# Сервис для обработки событий от датчиков

## Разработка
 - Требуется python >= 3.11
 - Устанавливаем poetry: `pip install poetry`
 - Устанавливаем зависимости: `poetry install`

## Локльный запуск
 - После установки зависимостей запуск сервиса: `fastapi dev app/main.py`
 - Для запуска бд в docker: 
 ```docker run --name event_handler_db -p 5432:5432 -e POSTGRES_USER=event_handler -e POSTGRES_PASSWORD=111111 -e POSTGRES_DB=event_handler_db -d -v "/absolute/path/to/directory-with-init-scripts":/docker-entrypoint-initdb.d postgres:16```
