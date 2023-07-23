#!/bin/sh
docker-compose -f billing/production.yml down
docker-compose -f billing/production.yml run --rm django python manage.py createsuperuser
