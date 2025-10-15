.PHONY: up down restart

up:
	docker compose up --build -d

down:
	docker compose down -v

restart:
	$(MAKE) down
	$(MAKE) up

.PHONY: rebuild-pre-commit  # устанавливает pre-commit + commit-msg хуки

	pre-commit clean && pre-commit install --hook-type commit-msg

.PHONY: tests

tests:
	pytest -svv tests/
