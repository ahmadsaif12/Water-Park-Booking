#!/bin/bash

set -e

# Wait for database
echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Fix permissions for volumes (running as root)
echo "Fixing permissions for Celery..."
chown -R waterpark:waterpark /vol/static /vol/media
chmod -R 775 /vol/static /vol/media

# Run Celery command as waterpark user
echo "Starting Celery..."
exec gosu waterpark "$@"
