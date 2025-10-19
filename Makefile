.PHONY: up down restart

up:
	docker compose run --rm migrate && docker compose up -d --build web-server nginx

down:
	docker compose down -v

restart:
	$(MAKE) down
	$(MAKE) up

.PHONY: rebuild-pre-commit  # устанавливает pre-commit + commit-msg хуки

rebuild-pre-commit:
	pre-commit clean && pre-commit install --hook-type commit-msg

.PHONY: tests

tests:
	pytest -svv tests/
