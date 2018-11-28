SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: build

.PHONY: build
build: ## Create Virtualenv and installs Ansible via Pip
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	virtualenv -p python2 .
	bin/pip install pip --upgrade
	bin/pip install -r requirements.txt --upgrade
	bin/buildout

.PHONY: build-plone5
build-plone5: ## Create Virtualenv and installs Ansible via Pip
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	virtualenv -p python2 .
	bin/pip install pip --upgrade
	bin/pip install -r requirements.txt --upgrade
	bin/buildout -c plone-5.2.x.cfg

.PHONY: clean
clean: ## Remove old Virtualenv and creates a new one
	@echo "Clean"
	rm -rf .eggs bin eggs develop-eggs lib parts include share .Python .installed.cfg .mr.developer.cfg

.PHONY: test
test: ## Run Tests
	@echo "$(GREEN)==> Run Tests$(RESET)"
	bin/test --xml

.PHONY: test-robot
test-robot: ## Run Tests
	@echo "$(GREEN)==> Run Robot Tests$(RESET)"
	bin/test --all --xml
