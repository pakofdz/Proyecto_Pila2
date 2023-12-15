#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations store
python manage.py migrate store

python manage.py createsuperuser --username=admin --email=sebaskirgaya@example.com --noinput

exec "$@"