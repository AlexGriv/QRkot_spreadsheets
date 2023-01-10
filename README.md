# Приложение QRKot

## Описание

Учебный проект во фреймворке FastAPI

**QRkot** - это API сервиса по сбору средств для финансирования благотворительных проектов. В сервисе реализована возможность регистрации пользователей, добавления благотворительных проектов и пожертвований, которые распределяются по открытым проектам.

Настроено автоматическое создание первого суперпользователя при запуске проекта.

## Ключевые технологии и библиотеки:
- [Python](https://www.python.org/);
- [FastAPI](https://fastapi.tiangolo.com/);
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/);
- [Alembic](https://pypi.org/project/alembic/);
- [Pydantic](https://pypi.org/project/pydantic/);

## Установка
1. Склонируйте репозиторий:
```
https://github.com/AlexGriv/cat_charity_fund.git
```
2. Активируйте venv и установите зависимости, необходимая версия Python >= 3.9:
```
python -m venv venv
source venv/Scripts/activate
python -m pip install -U pip
pip install -r requirements.txt
```
3. Создайте в корневой директории файл .env со следующим наполнением:
```
APP_TITLE=QRkot
APP_DESCRIPTION=Сервис поддержки котиков
DATABASE_URL='sqlite+aiosqlite:///./fastapi.db'
SECRET=<secret>
FIRST_SUPERUSER_EMAIL=<email superuser>
FIRST_SUPERUSER_PASSWORD=<password superuser>

```
4. Примените миграции для создания базы данных SQLite если потребуется:
```
alembic init --template async alembic
alembic revision --autogenerate -m "First migration"
alembic upgrade head
```
5. Проект готов к запуску.

Для локального запуска выполните команду:
```
uvicorn app.main:app --reload
```
Сервис будет запущен и доступен по следующим адресам:
- http://127.0.0.1:8000 - API
- http://127.0.0.1:8000/docs - автоматически сгенерированная документация Swagger

### Автор
AlexGriv
https://github.com/AlexGriv

