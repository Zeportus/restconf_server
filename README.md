# RESTCONF Server

Минималистичный YANG/RESTCONF-сервер на Python.  
Реализует базовый функционал по спецификациям [RFC 7950](https://datatracker.ietf.org/doc/html/rfc7950) и [RFC 8040](https://datatracker.ietf.org/doc/html/rfc8040):

- Загрузка и парсинг YANG-модулей (например, jukebox.yang).
- RESTCONF HTTP API (GET, PATCH, POST).
- Поддержка RPC вызовов, определённых в YANG-модели.
- Валидация данных при загрузке и изменении.

## Установка и запуск

1. Клонируйте репозиторий:

`git clone https://github.com/Zeportus/restconf_server.git`

`cd restconf_server`

2. Установите пакет (Не забудьте создать отдельное виртуальное окружение, если необходимо):

`pip install source/restconf_service_pkg`

3. Запустите сервис с указанием пути до конфигурационного .env файла (В репозитории имеется по умолчанию):

`restconf-service-run --config-path config/.env`


## Тестирование

1. GET /restconf/data/<path>:

`curl -v 'http://localhost:8085/restconf/data/example-jukebox:jukebox/library/artist=Miles%20Davis/album=Kind%20of%20Blue/admin' -H 'Accept: application/yang-data+json'`

2. PATCH /restconf/data/<path>:

`curl -v -X PATCH 'http://localhost:8085/restconf/data/example-jukebox:jukebox/library/artist=Miles%20Davis/album=Kind%20of%20Blue/admin' -H 'Accept: application/yang-data+json' -H 'Content-Type: application/yang-data+json' -d '{"label": "NEW LABEL"}'`

`curl -v 'http://localhost:8085/restconf/data/example-jukebox:jukebox/library/artist=Miles%20Davis/album=Kind%20of%20Blue/admin' -H 'Accept: application/yang-data+json'`

3. POST /restconf/operations/<rpc-name>:

`curl -v -X POST 'http://localhost:8085/restconf/operations/example-jukebox:play' -d '{"input": {"playlist": "bla bla", "song-number": 2}}' -H 'Accept: application/yang-data+json' -H 'Content-Type: application/yang-data+json'`

Посмотреть в логи сервиса, увидеть строчку:

`INFO:restconf_service.rpc_handlers.jukebox_rpc_handler_stub:Handle rpc "play" with args: playlist='bla bla' song_number=2`
