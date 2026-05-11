# Include .env if it exists
ifneq ("$(wildcard .env)","")
    include .env
    export
endif

.PHONY: build up down restart logs ps shell python enter migrations migrate superuser test clean fresh db-shell db-backup

# Default target
all: up

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps

shell:
	docker compose exec web python manage.py shell

python: shell

enter:
	docker compose exec web sh

db-shell:
	docker compose exec db psql -U $(DB_USER) -d $(DB_NAME)

db-backup:
	docker compose exec db pg_dump -U $(DB_USER) $(DB_NAME) > backup_$(shell date +%Y%m%d_%H%M%S).sql

migrations:
	docker compose exec web python manage.py makemigrations

migrate:
	docker compose exec web python manage.py migrate

superuser:
	docker compose exec web python manage.py createsuperuser

test:
	docker compose exec web python manage.py test

# Remove all containers and volumes
clean:
	docker compose down -v

# Completely fresh build and start (handles permission issues)
fresh:
	docker compose down -v
	docker compose build --no-cache
	docker compose up -d
	docker compose logs -f
