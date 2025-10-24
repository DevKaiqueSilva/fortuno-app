#!/bin/bash
set -e

echo "=== Environment Variables ==="
echo "PORT: $PORT"
echo "DATABASE_URL exists: $([ -n "$DATABASE_URL" ] && echo "YES" || echo "NO")"
echo "RAILWAY_ENVIRONMENT: $RAILWAY_ENVIRONMENT"

if [ -z "$DATABASE_URL" ]; then
    echo "WARNING: DATABASE_URL not set, using SQLite"
else
    echo "Using PostgreSQL database"
fi

echo "=== Testing Django setup ==="
python manage.py check

echo "=== Running migrations ==="
python manage.py migrate

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Starting Gunicorn ==="
exec gunicorn fortuno.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 30 \
    --log-level info