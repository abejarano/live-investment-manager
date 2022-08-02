#!/bin/bash



echo "Collect static files"
python /app/manage.py collectstatic --no-input --clear
python /app/manage.py makemigrations crypto investment
python /app/manage.py migrate

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    python /app/manage.py createsuperuser --no-input
fi

exec "$@"
