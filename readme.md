# A simple online catalog for NDA company
This is a small django application, introducing online catalog
of products with categories and brands. In plans: a cart and mail notifications services

## Pre-requisites
- python 3.8+ installed
- psql connection available

## Installation:
```shell
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration:
1. Create .env file and populate it with values. Please check .env.example for reference
2. Run initial database commands: 
    ```shell
    python3 manage.py migrate
    python3 manage.py createsuperuser
    ```
3. Run collect static command
    ```shell
    python3 manage.py collectstatic
    ```
4. How to sync migrations and database
   ```shell
   pg_restore -U postgres -h 0.0.0.0 -d xxxx < dump.dump --disable-triggers
   rm -rf catalog/migrations
   rm -rf files/migrations
   python manage.py makemigrations
   python manage.py migrate
   pg_dump --column-inserts --data-only -h 0.0.0.0 -U postgres -W -Fc xxxx > dump.dump
   ```
replace "xxxx" with DB_NAME and "postgres" with your DB_USER
5. Redis
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

## Run the app
```shell
python3 manage.py runserver
```