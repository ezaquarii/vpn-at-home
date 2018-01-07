ENV := "env"
PYTHON := $(ENV)/bin/python3
PIP := $(ENV)/bin/pip3

.PHONY: install configure

all:
	@echo "Welcome to OpenVPN@Home make system"
	@echo ""
	@echo "Available targets:"
	@echo " * devel     - boostrap project for development (your first choice)"
	@echo " * install   - install virtual environment and all dependencies"
	@echo " * distclean - clean project, delete all data (start from 'git clone' state)"
	@echo " * runserver - start development server"
	@echo " * test      - run full test suite"

devel: install configure
	$(PYTHON) manage.py bootstrap

install: $(ENV)
	$(PIP) install -U setuptools
	$(PIP) install deps/django_x509-0.3.5a0-py2.py3-none-any.whl
	$(PIP) install -r requirements.txt

configure: install
	$(PYTHON) manage.py configure -d

$(ENV):
	@echo "Creating Python virtual environemnt"
	virtualenv -p python3 --no-setuptools $(ENV)

test:
	$(PYTHON) manage.py test

runserver:
	$(PYTHON) manage.py runserver 8001

distclean:
	@[ -d openvpnathome ];
	rm -f db.sqlite3
	rm -rf env
	rm -f openvpnathome/config.py
	@echo "All backend data deleted."
