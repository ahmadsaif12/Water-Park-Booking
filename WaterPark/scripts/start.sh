#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for database
echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Fix permissions for volumes (running as root)
echo "Fixing permissions..."
chown -R waterpark:waterpark /vol/static /vol/media
chmod -R 775 /vol/static /vol/media

# Apply database migrations
echo "Applying database migrations..."
gosu waterpark python manage.py migrate

# Collect static files
echo "Collecting static files..."
# Clear existing static files to avoid permission issues with old files
gosu waterpark python manage.py collectstatic --no-input --clear

# Start Gunicorn or Dev Server
if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ]; then
    echo "Starting development server..."
    exec gosu waterpark python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn..."
    exec gosu waterpark gunicorn WaterPark.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers ${GUNICORN_WORKERS:-4} \
        --threads ${GUNICORN_THREADS:-2} \
        --access-logfile - \
        --error-logfile -
fi
