#!/bin/sh
set -e

until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "Esperando a PostgreSQL..."
  sleep 1
done

python manage.py migrate --noinput

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

python manage.py runserver 0.0.0.0:8000
