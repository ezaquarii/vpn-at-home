VIRTUALENV ?= "$(CURDIR)/../env"
PYTHON := $(VIRTUALENV)/bin/python3
PIP := $(VIRTUALENV)/bin/pip3

.PHONY: install configure virtualenv

all:
	@echo "Welcome to VPN@Home make system"
	@echo ""
	@echo "Available targets:"
	@echo " * devel      - boostrap project for development (your first choice)"
	@echo " * virtualenv - install virtual environment and all dependencies"
	@echo " * runserver  - start development server"
	@echo " * test       - run full test suite"
	@echo
	@echo "Python virtualenv installed in VIRTUALENV = $(VIRTUALENV)"

devel: virtualenv
	$(PYTHON) manage.py configure --devel
	$(PYTHON) manage.py migrate
	$(PYTHON) manage.py set_admin admin@localhost admin1234

virtualenv: $(VIRTUALENV)

$(VIRTUALENV):
	@echo
	@echo "Creating Python virtual environemnt"
	@echo "Destination: $(VIRTUALENV)"
	@echo
	virtualenv -p python3 --no-setuptools $(VIRTUALENV)
	$(PIP) install -U setuptools
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) manage.py test

runserver:
	$(PYTHON) manage.py runserver --insecure 8001

