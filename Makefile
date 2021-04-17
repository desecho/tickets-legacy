PROJECT := tickets

export 

.DEFAULT_GOAL := help

SHELL := /bin/bash
SOURCE_CMDS := source venv/bin/activate && source env.sh

#------------------------------------
# Help
#------------------------------------
TARGET_MAX_CHAR_NUM := 25

# COLORS
RED     := \033[0;31m
GREEN   := \033[0;32m
YELLOW  := \033[0;33m
BLUE    := \033[0;34m
MAGENTA := \033[0;35m
CYAN    := \033[0;36m
WHITE   := \033[0;37m
RESET   := \033[0;10m

.PHONY: help
## Show help | Help
help:
	@echo ''
	@echo 'Usage:'
	@printf "  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}"
	@echo ''
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
		    if (index(lastLine, "|") != 0) { \
				stage = substr(lastLine, index(lastLine, "|") + 1); \
				printf "\n ${GRAY}%s: \n", stage;  \
			} \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			if (index(lastLine, "|") != 0) { \
				helpMessage = substr(helpMessage, 0, index(helpMessage, "|")-1); \
			} \
			printf "    ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
#------------------------------------

#------------------------------------
# Installation
#------------------------------------

.PHONY: bootstrap
## Bootstrap project | Installation
bootstrap: create-db bower-install docker-build syncdb migrate 

.PHONY: bower-install
## Bower install
bower-install: 
	bower install

.PHONY: create-db
## Create db
create-db:
	source db_env.sh && \
	scripts/create_db.sh

#------------------------------------
# Development commands
#------------------------------------

.PHONY: drop-db
## Drop db | Development
drop-db:
	source db_env.sh && \
	scripts/drop_db.sh

#------------------------------------
# Docker commands
#------------------------------------
DOCKER_ENV_FILE := env_docker
export 
.PHONY: build
## Build images | Docker
build:
	docker build -t ${PROJECT} .
	docker build -t tickets_static docker_static

.PHONY: run
## Run server
run:
	docker-compose up

.PHONY: docker-sh
## Run docker shell
docker-sh:
	docker run -ti --env-file ${DOCKER_ENV_FILE} ${PROJECT} sh

.PHONY: syncdb
## Run syncdb command
syncdb:
	docker run -ti --add-host host.docker.internal:host-gateway --env-file ${DOCKER_ENV_FILE} ${PROJECT} ./manage.py syncdb

.PHONY: migrate
## Run migrate command
migrate:
	docker run -ti --add-host host.docker.internal:host-gateway --env-file ${DOCKER_ENV_FILE} ${PROJECT} ./manage.py migrate

#------------------------------------
