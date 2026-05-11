#!/bin/bash
set -e

# Permissions for volumes
chown -R waterpark:waterpark /vol/static /vol/media
chmod -R 775 /vol/static /vol/media

# Database and Static Files
gosu waterpark python manage.py migrate --noinput
gosu waterpark python manage.py collectstatic --noinput --clear

# Start Server
if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ]; then
    exec gosu waterpark python manage.py runserver 0.0.0.0:8000
else
    exec gosu waterpark gunicorn WaterPark.wsgi:application --bind 0.0.0.0:8000 --workers 4
fi
