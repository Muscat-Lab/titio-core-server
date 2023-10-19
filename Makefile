.PHONY: all
all:


.PHONY: format
format:
	docker-compose exec fastapi /bin/bash -c "poetry run isort ."
	docker-compose exec fastapi /bin/bash -c "poetry run black . --experimental-string-processing"
	docker-compose exec fastapi /bin/bash -c "poetry run ruff check ."
	docker-compose exec fastapi /bin/bash -c "poetry run mypy ."


.PHONY: migration_init
migration_init:
	docker-compose exec fastapi /bin/bash -c "poetry run alembic upgrade head"


.PHONY: server
server:
	python -m server