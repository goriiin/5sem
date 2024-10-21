BINARY_NAME=server
DOCKER_COMPOSE_FILE = docker-compose.yml
DOCKER_COMPOSE = sudo docker compose


default: help

help:
	@echo 'использование:sudo make [target]'
	@echo 'targets:'
	@echo '   build - компиляция образа django'
	@echo '   refresh - перекомпиляция образа'
	@echo '   run - поднимает все контейнеры'


build:
	sudo docker build -t app-image .

refresh:
	sudo docker stop app && docker rm app && docker rmi app-image && docker compose up -docker

run:
	$(DOCKER_COMPOSE) up -d

# Target to restart Gunicorn container
restart-gunicorn:
	$(DOCKER_COMPOSE) restart gunicorn

# Target to restart Nginx container
restart-nginx:
	sudo docker stop nginx-app && docker rm nginx-app && docker rmi nginx-app-image && docker compose up -docker

down:
	$(DOCKER_COMPOSE) down

.PHONY: clean build