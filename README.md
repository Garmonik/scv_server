# Документация

## Стек
* Django
* Django Rest Framework
* drf_spectacular
* Docker
* docker-compose

## Swagger
Для документирования API удобно использоввать Swagger. Для этого использовался drf_spectacular, а все необходимые настройки были прописаны в файле csvtest/schema_urls.py:

```python
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

Для перехода в [Swagger](http://127.0.0.1:8000/api/schema/swagger-ui/#/) необходимо запустить сервер и перейти по следующему url http://127.0.0.1:8000/api/schema/swagger-ui/#/.
Swagger актуализирован для всех API в этом проекте.

## API

### http://127.0.0.1:8000/api/upload/

URL для вызова API, которое должно принимать из запроса .csv файлы для обработки типовых deals.csv файлов, содержащих истории сделок и сохранять извлеченные из файла данные в БД проекта

method: POST

body: deals: file

response:  

status_code = 200:
```json
{
  "status": "OK"
}
```

status_code = 400:
```json
{
  "status": "Error",
  "desc": "Some error"
}
```

### http://127.0.0.1:8000/api/top-clients/

URL для вызова API, которое должно в ответ на запрос возвращать поле “response” со списком из 5 клиентов, потративших наибольшую сумму за весь период.
Каждый клиент описывается следующими полями:
* **username** - логин клиента;
* **spent_money** - сумма потраченных средств за весь период;
* **gems** - список из названий камней, которые купили как минимум двое из списка "5 клиентов, потративших наибольшую сумму за весь период", и данный клиент является одним из этих покупателей.

method: GET



response:  

status_code = 200:
```json
{
  "response": [
    {
      "username": "username",
      "spent_money": 99999.00,
      "gems": [
        "Элемент 1",
        "Элемент 2",
        "Элемент 3",
        "Элемент 4",
        "Элемент 5"
      ]
    }
  ]
}
```

status_code = 400:
```json
{
  "status": "Error",
 "desc": "The start date cannot be greater than the end date."
}
```

## Кэширование

Для кэширования в GET-запросе используется декоратор:

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 5))
def get(self, request):
    ...
```

Данный декоратор кэширует запрос и сохраняем информацию об этом запросе на 5 минут.

## Запуск проекта

### Способ №1

Приложение можно запустить просто через консоль с помощью команды:

```
python3 manage.py runserver
```

Таким образом мы запустим синхронный сервер. Вы должны находится в папке, где лежит manage.py!!!

### Способ №2

Приложение можно запустить просто через консоль с помощью команды:

```
gunicorn csvtest.wsgi:application --workers 4
```

Таким образом мы запустим сервис django, который работает на многопоточном WSGI-сервере. Вы должны находится в папке, где лежит manage.py!!!

### Способ №3

Приложение можно запустить просто через docker-compose:

В основной папке проекта запустите команду
```
docker-compose up
```

аким образом мы запустим синхронный сервер.

### Способ №4

Приложение можно запустить просто через docker-compose:

Для начала измените файл docker-compose.yml:
```yml
services:
  web_app:
    build:
      context: .
    ports:
      - "8000:8000"
    volumes:
      - ./service:/service

    command: >
      sh -c "python3 manage.py runserver 0.0.0.0:8000"
```
На следующий код:
```yml
services:
  web_app:
    build:
      context: .
    ports:
      - "8000:8000"
    volumes:
      - ./service:/service

    command: >
      sh -c "gunicorn csvtest.wsgi:application --workers 4"
```

В основной папке проекта запустите команду

```
docker-compose up
```

Таким образом мы запустим сервис django, который работает на многопоточном WSGI-сервере.