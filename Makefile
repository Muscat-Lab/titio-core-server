.PHONY: all
all:


.PHONY: format
format:
	docker-compose exec fastapi /bin/bash -c "poetry run isort ."
	docker-compose exec fastapi /bin/bash -c "poetry run black ."
	docker-compose exec fastapi /bin/bash -c "poetry run mypy ."
