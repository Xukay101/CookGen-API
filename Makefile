.PHONY: migrate upgrade docker-migrate docker-upgrade docker-init-data build

# Migrations 

migrate:
	alembic revision --autogenerate -m "Update database"

upgrade:
	alembic upgrade head

# Migrations Docker Compose

docker-migrate:
	docker-compose run api alembic revision --autogenerate -m "Update database through Docker"

docker-upgrade:
	docker-compose run api alembic upgrade head

# Init Data

docker-init-data:
	docker-compose run api python -m app.init_data

# Build

build:
	docker-compose up --build -d
	sleep 10
	make docker-upgrade
	make docker-init-data