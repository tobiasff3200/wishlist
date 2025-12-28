#!/bin/bash
set -e
cd /app || exit

echo "----- Collect static files ------ " 
python manage.py collectstatic --noinput

echo "-----------Apply migration--------- "
if python manage.py showmigrations --plan | grep -q "\[ \]"; then
  echo "Applying database migrations..."
  python manage.py migrate --noinput
else
  echo "No migrations needed"
fi

echo "Checking database consistency..."
python manage.py makemigrations --check --dry-run

echo "-----------Run gunicorn--------- "
export DJANGO_SETTINGS_MODULE=core.settings
gunicorn -b :8000 core.wsgi:application
