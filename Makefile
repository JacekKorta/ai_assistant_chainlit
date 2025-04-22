.PHONY: all chainlit-exec down help migrate nginx-exec postgres-exec prisma-cli-exec up upd web-exec web-makemigrations web-migrate web-test

all: up ## Run 'up' target by default

help: ## Show this help message
	@echo "\nSpecify a command. The choices are:\n"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""

chainlit-exec: ## Enter the chainlit container shell
	docker-compose exec chainlit bash

down: ## Stop and remove containers, networks, volumes
	docker-compose down

nginx-exec: ## Enter the nginx container shell
	docker-compose exec nginx bash

postgres-exec: ## Enter the postgres container shell
	docker-compose exec postgres bash

prisma-cli-exec: ## Enter the prisma_cli container shell
	docker-compose exec prisma_cli bash

up: ## Run all containers in foreground
	docker-compose up

upd: ## Run all containers in detached mode (background)
	docker-compose up -d

web-exec: ## Enter the web (Django) container shell
	docker-compose exec web bash

web-makemigrations: ## Create new Django database migrations inside the web container
	docker-compose exec web python manage.py makemigrations

web-migrate: ## Run Django database migrations inside the web container
	docker-compose exec web python manage.py migrate

web-test: ## Run Django tests inside the web container, keeping the test database
	docker-compose exec web python manage.py test --keepdb