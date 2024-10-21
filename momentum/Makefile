BINARY_NAME=server

S=sudo

DC = docker compose
STOP = docker stop
LOG = docker logs

RM = docker rm
RMI = docker rmi

NGINX_app = nginx-app
NGINX_image = nginx-app-image
GUNI_app=g-app
GUNI_image=g-app-image
APP = app
APP_image =app-image


default: help

help:
	@echo 'Использование: sudo make [target]'
	@echo ''
	@echo 'Сборка и установка:'
	@echo '   build - компиляция образа django'
	@echo '   install - установка зависимостей'
	@echo '   save - сохранение зависимостей в requirements.txt'
	@echo ''
	@echo 'Запуск и управление контейнерами:'
	@echo '   run - поднимает все контейнеры'
	@echo '   r-nginx - перезапускает контейнер nginx'
	@echo '   r-guni - перезапускает контейнер gunicorn'
	@echo '   r-app - перезапускает контейнер приложения'
	@echo '   r-all - перезапускает все контейнеры'
	@echo ''
	@echo 'Просмотр логов и списка контейнеров:'
	@echo '   log-nginx - показывает лог контейнера nginx'
	@echo '   log-guni - показывает лог контейнера gunicorn'
	@echo '   log-app - показывает лог контейнера приложения'
	@echo '   ps - показывает список работающих контейнеров'
	@echo '   psa - показывает список всех контейнеров'
	@echo ''
	@echo 'Остановка и удаление контейнеров:'
	@echo '   down - останавливает и удаляет все контейнеры'
	@echo '   rm-all - удаляет все контейнеры'




install:
	pip install -r requirements.txt

app-run:
	python3 manage.py runserver

guni-run:
	gunicorn -b 0.0.0.0:9009 momentum.wsgi:application &

rm-all:
	$(S) $(STOP) $(NGINX_app) $(APP) && $(S) $(RM) $(NGINX_app)

save:
	pip freeze > requirements.txt

ps:
	$(S) docker ps

psa:
	$(S) docker ps -a

build:
	$(S) docker build -t app-image .

run:
	$(S) $(DC) up -d

r-nginx:
	$(S) $(STOP) $(NGINX_app) && $(RM)  $(NGINX_app) && $(RMI) $(NGINX_image) && $(DC) up -d

r-guni:
	$(S) $(STOP) $(GUNI_app) && $(RM) $(GUNI_app) && $(RMI) $(GUNI_image) && $(DC) up -d

r-app:
	$(S) $(STOP) $(APP) && $(RM) $(APP) && $(RMI) $(APP_image) && $(DC) up -d

r-all:
	$(S) make r-nginx
	$(S) make r-guni
	$(S) make r-app

log-nginx:
	$(S) $(LOG) $(NGINX_app)

log-guni:
	$(S) $(LOG) $(GUNI_app)

log-app:
	$(S) $(LOG) $(APP)

down:
	$(S) $(DC) down

.PHONY: clean build
