#!/bin/bash
cd /app || exit

echo "----- Collect static files ------ " 
python manage.py collectstatic --noinput

echo "-----------Apply migration--------- "
python manage.py migrate

echo "-----------Run gunicorn--------- "
export DJANGO_SETTINGS_MODULE=core.settings
gunicorn -b :8000 core.wsgi:application
