.PHONY: up down

up:
	docker compose up --build -d

down:
	docker compose down -v

.PHONY: restart

restart:
	$(MAKE) down
	$(MAKE) up

.PHONY: rebuild-pre-commit  # устанавливает pre-commit + commit-msg хуки

	pre-commit clean && pre-commit install --hook-type commit-msg
