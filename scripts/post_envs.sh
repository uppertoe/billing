cd ~
docker-compose -f billing/production.yml --verbose build

echo "Users must be migrated separately"
docker-compose -f billing/production.yml run --rm django python manage.py migrate users --skip-checks
docker-compose -f billing/production.yml run --rm django python manage.py migrate --skip-checks
