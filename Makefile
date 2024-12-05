.PHONY: all create-env build up migrate

all: create-env build up migrate

create-env:
	@echo "# Django" > .env
	@echo 'SECRET_KEY="develop"' >> .env
	@echo "" >> .env
	@echo "# Postgres" >> .env
	@echo 'POSTGRES_NAME="postgres"' >> .env
	@echo 'POSTGRES_USER="postgres"' >> .env
	@echo 'POSTGRES_PASSWORD="postgres"' >> .env
	@echo 'POSTGRES_HOST="db"' >> .env
	@echo 'POSTGRES_PORT="5432"' >> .env
	@echo 'REDIS_URL="redis://redis:6379/0"' >> .env
	@echo 'API_ID=123' >> .env
	@echo 'API_HASH=123' >> .env
	@echo 'BOT_TOKEN=pass'>> .env
	@echo ".env file created successfully."

build:
	@docker-compose build
	@echo "Docker containers built successfully."

up:
	@docker-compose up -d
	@echo "Docker containers started successfully."

migrate:
	@docker-compose exec django python manage.py migrate
	@echo "Database migrated successfully."
