.PHONY: migrate upgrade docker-migrate docker-upgrade

# Migraciones sin Docker Compose

migrate:
	alembic revision --autogenerate -m "Update database"

upgrade:
	alembic upgrade head

# Migraciones con Docker Compose

docker-migrate:
	docker-compose run api alembic revision --autogenerate -m "Update database through Docker"

docker-upgrade:
	docker-compose run api alembic upgrade head