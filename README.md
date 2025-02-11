# web-test

## О проекте:
- Позволяет получить вопросы для викторины с внешнего API
- Дает возможность конвертировать файл из .wav в .mp3

## О проекте (технически):
- Использует луковую архитектуру
- Настроено логирование для дальнейшей интеграции в ELK-stack/Grafana Loki
- Асинхронный доступ к БД
- Асинхронный доступ к ручкам

## Стек
```
- FastAPI
- Sqlalchemy
- Logging
- Postgresql
- Docker
- Asyncio
- PyDub
- Pipenv
```

## Инструкция по сборке с примерами данных:
1. Создать файл .env в корне проекта
2. Необходим записать переменные для подключения к бд:
```
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=quiz
DATABASE_HOST=db
DATABASE_PORT=5432
```