.PHONY: migrate upgrade

migrate:
	alembic revision --autogenerate -m "Update database"

upgrade:
	alembic upgrade head