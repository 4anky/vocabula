.PHONY: up down

up:
	docker compose up --build -d

down:
	docker compose down -v

.PHONY: restart

restart:
	$(MAKE) down
	$(MAKE) up
