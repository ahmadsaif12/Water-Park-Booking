ifneq ("$(wildcard .env)","")
    include .env
    export
endif

.PHONY: up down down-v restart build logs ps shell enter migrate migrations superuser test db-shell

up:
	docker compose up -d

down:
	docker compose down

down-v:
	docker compose down -v

restart:
	docker compose restart

build:
	docker compose build

logs:
	docker compose logs -f

ps:
	docker compose ps

shell:
	docker compose exec web python manage.py shell

enter:
	docker compose exec web bash

migrate:
	docker compose exec web python manage.py migrate

migrations:
	docker compose exec web python manage.py makemigrations

superuser:
	docker compose exec web python manage.py createsuperuser

test:
	docker compose exec web python manage.py test

db-shell:
	docker compose exec db psql -U $(DB_USER) -d $(DB_NAME)
