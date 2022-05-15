release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn snowcore.wsgi --workers 1
