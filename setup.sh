#!/bin/sh

cd ./experimental/
python3 -m pip install -r requirements.txt
djangokey=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
env="DJANGOKEY=\"${djangokey}\""
touch .env 
echo ${env} > .env
python manage.py runserver
