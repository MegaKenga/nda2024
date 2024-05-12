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

squashcatalog:
		python3 manage.py squashmigrations catalog

flushredis:
		redis-cli flushall
