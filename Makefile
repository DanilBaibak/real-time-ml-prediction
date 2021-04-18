SHELL=/bin/bash

init:
		cp .env.public .env

up:
		@docker-compose -f docker-compose-local.yml up

stop:
		@docker-compose -f docker-compose-local.yml stop

down:
		@docker-compose -f docker-compose-local.yml down --rmi local --volumes
		@make clean

restart:
		@make -k stop
		@make -k down
		@make -k up

bash:
		@docker exec -it rest_ml bash -c "bash"

clean:
		@find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf
		@rm -rf .mypy_cache
		@rm -rf .pytest_cache

lint:
		@python3 -m flake8 --max-line-length 120 ./src
		@python3 -m mypy --no-warn-no-return --ignore-missing-imports ./src
