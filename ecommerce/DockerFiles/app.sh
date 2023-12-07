#!bin/bash

pip install gunicorn

python manage.py makemigrations

python manage.py migrate

gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000