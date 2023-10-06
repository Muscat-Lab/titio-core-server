.PHONY: all
all:


.PHONY: format
format:
	docker-compose exec fastapi /bin/bash -c "poetry run isort ."
	docker-compose exec fastapi /bin/bash -c "poetry run black . --experimental-string-processing"
	docker-compose exec fastapi /bin/bash -c "poetry run ruff check ."
	docker-compose exec fastapi /bin/bash -c "poetry run mypy ."
