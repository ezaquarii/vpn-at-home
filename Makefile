SHELL := /bin/bash
PATH := $(PWD)/bin:$(PATH)
ENV := env
PYTHON := $(ENV)/bin/python3

.PHONY: devel devel_backend distclean runserver install install_backend install_virtualenv install_etc deb install_deb uninstall_deb

all:
	@echo "Welcome to VPN@Home make system"
	@echo
	@echo "Available top-level targets:"
	@echo " * devel              - bootstrap both projects for development"
	@echo "   * devel_backend    - bootstrap backend for development (dependency of devel)"
	@echo "   * devel_frontend   - bootstrap frontend for development (dependency of devel)"
	@echo " * distclean          - clean projects, delete all data (start from 'git clone' state)"
	@echo " * runserver          - run development server (manage.py runserver)"
	@echo " * deb                - build debian package"
	@echo "   * remove_deb       - remove installed Debian package"
	@echo "   * purge_deb        - purge installed Debian package"
	@echo "   * install_deb      - install previously built debian package"
	@echo " * install_build_deps - convenient shortcut to install deb build dependencies"

devel: devel_backend devel_frontend
	@echo "Development environment is ready"

devel_backend: env
	env/bin/init.sh --no-smtp --development admin@localhost admin1234

devel_frontend:
	$(MAKE) -C frontend build-devel

distclean:
	@echo
	@echo "Cleaning working directory"
	@echo
	git clean -fdx

env:
	python3 -m venv env
	$(PYTHON) env/bin/pip install --no-cache --no-index --find-links=pypi -r requirements.txt
	ln -s $(CURDIR)/backend/vpnathome "`find env -name site-packages`"
	ln -sr bin/manage.py env/bin/
	ln -sr bin/deploy_vpn.sh env/bin/
	ln -sr bin/inventory.sh env/bin/
	ln -sr bin/init.sh env/bin/

docker:
	docker build -t vpnathome .

install_build_deps:
	sudo apt install \
		debhelper \
		make \
		python3 \
		python3-pip \
		python3-dev \
		python3-wheel \
		python3-venv \
		devscripts \
		debhelper \
		sudo \
		dh-virtualenv \
		libffi-dev \
		libssl-dev \
		openvpn \
		openssh-client \
		ansible

	@echo
	@echo "You still need recent version of node.js. Use NVM to install it as the packaged version is too old."
	@echo "Current recommended version is 10 (latest LTS)".
	@echo

deb:
	git clean -fdx
	debuild --no-lintian -i -uc -us -b

install_deb:
	sudo dpkg -i ../vpnathome*.deb

remove_deb:
	sudo dpkg --remove vpnathome

purge_deb:
	sudo dpkg --purge vpnathome

runserver:
	$(PYTHON) env/bin/manage.py runserver --insecure 8001

test_backend:
	$(PYTHON) env/bin/manage.py test vpnathome

test_frontend:
	$(MAKE) -C frontend test
