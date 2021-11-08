#!/bin/bash
source /venv/bin/activate
cd /app

echo "----- Collect static files ------ " 
python manage.py collectstatic --noinput

echo "-----------Apply migration--------- "
python manage.py makemigrations 
python manage.py migrate

echo "-----------Run gunicorn--------- "
export DJANGO_SETTINGS_MODULE=wishlist.settings
gunicorn -b :8000 wishlist.wsgi:application
