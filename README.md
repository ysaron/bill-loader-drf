# Bill Loader

## Локальная установка

### Требования
- Docker
- docker-compose

### Установка

Клонировать репозиторий:
```shell
git clone https://github.com/ysaron/bill-loader-drf.git
```

В корне проекта создать `.env.dev` и задать в нем следующие переменные окружения:
```dotenv
DEBUG=1
SECRET_KEY="<your_secret_key>"
DJANGO_ALLOWED_HOSTS=".localhost 127.0.0.1 [::1]"
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=local_db
SQL_USER=local_user
SQL_PASSWORD=local_password
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

Сборка образа + запуск:
```shell
docker-compose up -d --build
```

Загрузка файлов:
```shell
curl --upload-file "<path_to_files>/client_org.xlsx" http://127.0.0.1:8000/api/v1/upload/
curl --upload-file "<path_to_files>/bills.xlsx" http://127.0.0.1:8000/api/v1/upload/
```

Списки клиентов и счетов с фильтрацией доступны в браузере:  
http://127.0.0.1:8000/api/v1/clients/  
http://127.0.0.1:8000/api/v1/bills/  

----

При получении ошибки при запуске:
```shell
exec /usr/src/app/entrypoint.sh: no such file or directory
```

изменить окончания строк `entrypoint.sh` на Unix-тип (CRLF > LF).

