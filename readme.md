# Cайт-каталог компании НДА

## Требования
- python 3.8+ 
- postgresql
- redis
- celery

## Создание виртуального окружения и установка зависимостей:
```shell
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Конфигурация:
1. Создать файл .env и заполнить по подобию env.example
2. Создать миграции: 
    ```shell
    python3 manage.py migrate
    python3 manage.py createsuperuser
    ```
3. Собрать статику на продакшн сервере:
    ```shell
    python3 manage.py collectstatic
    ```

4. Redis
   start
   ```shell
   redis-server
   ```
   stop
   ```shell
   service redis-server stop 
   ```
   flush cache
   ```shell
   redis-cli flushall
   ```

## Запустить приложение:
```shell
python3 manage.py runserver
```