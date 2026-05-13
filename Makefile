start:
		python3 manage.py runserver

migrations:
		python3 manage.py makemigrations

migrate:
		python3 manage.py migrate

shell:
		python3 manage.py shell

admin:
		python3 manage.py createsuperuser

flushredis:
		redis-cli flushall

check:
        python3 manage.py check
