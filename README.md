# Inventory_management_system_Fast-API
![Python](https://img.shields.io/badge/-Python-f1f518?style=flat-square&logo=python)  
![FastAPI](https://img.shields.io/badge/-FastAPI-74cf3c?style=flat-square&logo=fastapi)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-ce62f5?style=flat-square&logo=bootstrap)
![Redis](https://img.shields.io/badge/-Redis-f78b97?style=flat-square&logo=redis) ![Pydantic](https://img.shields.io/badge/-Pydantic-E92063?style=flat-square&logo=Pydantic)
![Docker](https://img.shields.io/badge/-Docker-1de4f2?style=flat-square&logo=docker)  


Система управления запасами(материалами) предположим на складе
и автоматическая отправка заявки на email компаний(предварительно нужно добавить эти компании)
у которых есть данный материал. Используется nosql база данных, а конкретно Redis

- Проект состоит из двух частей:
1. API
2. WEB-часть проекта

## Установка

## Установка на локальный компьютер
- git clone https://github.com/Victor-Krupeichenko/Inventory_management_system_Fast-API.git
- pip install -r requirements.txt
- запуск через терминал:  uvicorn main:app --reload
- перейти по ссылке: http://127.0.0.1:8000 для api документации http://127.0.0.1:8000/docs

## Установка в docker
- git clone https://github.com/Victor-Krupeichenko/Inventory_management_system_Fast-API.git
- запуск через терминал(обязательно должны находится в папке проекта): docker compose up или docker-compose up
- перейти по ссылке: http://0.0.0.0:8001 для api документации http://0.0.0.0:8001/docs

! Необходимо создать в корне проекта файл .env в котором указать:
REDIS_HOST=app_redis(либо указать свой) - тогда необходимо изменить его и в docker-compose.yml
REDIS_PORT=6111(либо указать свой) - тогда необходимо изменить его и в docker-compose.yml
REDIS_DB=1(либо указать свою)

SECRET_KEY_TOKEN=указать_свой_секретный_ключ_которым_будет_шифроваться_токен
ALGORITHM_TOKEN=HS256
NAME_COOKIES=указать_имя_для_cookies
ACCESS_TOKEN_EXPIRE_DAYS=указать_срок_действия_токена

## Структура проекта
Папка api содержит:
- Папка company содержит:
  * Абстрактный клас интерфейса;
  * Модель company
  * Реализация интерфейса для взаимодействия с redis;
  * Endpoints для взаимодействия с моделью company;
  * Pydantic схему для валидации входных данных.
- Папка ordering содержит:
  * Абстрактный клас интерфейса для взаимодействия с redis;
  * Реализация интерфейса для взаимодействия с redis.
- Папка stock содержит:
  * Абстрактный клас интерфейса для взаимодействия с redis;
  * Модель stock;
  * Реализация интерфейса для взаимодействия с redis;
  * Endpoints для взаимодействия с моделью stock;
  * Pydantic схему для валидации входных данных.
- Папка users содержит:
  * Абстрактный клас интерфейса;
  * Модель user;
  * Реализация интерфейса для взаимодействия с redis;
  * Endpoints для взаимодействия с моделью user;
  * Pydantic схему для валидации входных данных;
  * Настройки имен переменного окружения для токена;
  * Создание токена и получение текущего пользователя
- Файл utils.py - вспомогательная функция для проверки того что вернула pydantic-схема

Папка docker_run_app содержит скрип который запускает приложение в docker

Папка web содержит:
- Папка static:
  * статический файл для навигационной панели
- Папка templates:
  * Папка _inc содержит подключаемые html-шаблоны
  * Основные html-шаблоны
- forms.py - получает поля из pydantic-схемы необходимые для рендеринга в html-форме
- routers.py - endpoints -> для взаимодействия с web-приложением
- web_utils.py - вспомогательные функции

Файл docker-compose.yml содержит описание запуска проекта в docker
Файл Dockerfile содержит инструкции для создания docker-образа
Файл main.py запускает само приложение
Файл requirements.txt в нем находятся все необходимые для работы приложения библиотеки и зависимости
Файл settings_env.py - настройки имен переменно окружения


## Контакты:
Виктор
# Email:
- krupeichenkovictor@gmail.com
- victor_krupeichenko@hotmail.com
# Viber:
- +375447031953 

