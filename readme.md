A simple online catalog for NDA company

installation:
sudo apt-get install python
python -m pip install Django


database postgres:
sudo apt install postgresql postgresql-contrib -y 
pip install psycopg2

makefile:
sudo apt install make

make start - run wsgi server
make migrations - run migrations
make migrate - apply migrations


dotenv:
pip install python-dotenv
in settings.py: 
import os
from dotenv import load_dotenv
load_dotenv()