DEVEL_VIRTUALENV_DIR=$(CURDIR)/env
DATABASE_DIR=$(CURDIR)/data/db
LOG_DIR=$(CURDIR)/data/logs
CONFIG_FILE=$(CURDIR)/data/settings.json
DJANGO_LOG_FILE=$(LOG_DIR)/django.log
DOCKER_BUILD?=false
INSTALL_ROOT=$(DESTDIR)/srv/vpnathome
INSTALL_VIRTUALENV=$(INSTALL_ROOT)/env
DEPLOYMENT_ROOT=/srv/vpnathome
DEPLOYMENT_VIRTUALENV=$(DEPLOYMENT_ROOT)/env/

.PHONY: devel distclean runserver install install_backend install_virtualenv install_etc deb install_deb uninstall_deb

all:
	@echo "Welcome to VPN@Home make system"
	@echo
	@echo "Env:"
	@echo " * DESTDIR:               (path) [$(DESTDIR)]"
	@echo " * INSTALL_ROOT:          (path) [$(INSTALL_ROOT)]"
	@echo " * DEPLOYMENT_ROOT:       (path) [$(DEPLOYMENT_ROOT)]"
	@echo " * DEPLOYMENT_VIRTUALENV: (path) [$(DEPLOYMENT_VIRTUALENV)]"
	@echo " * DOCKER_BUILD:          (bool) [$(DOCKER_BUILD)]"
	@echo
	@echo "Available top-level targets:"
	@echo " * devel            - bootstrap both projects for development"
	@echo "   * devel_backend  - bootstrap backend for development (dependency of devel)"
	@echo "   * devel_frontend - bootstrap frontend for development (dependency of devel)"
	@echo " * distclean        - clean projects, delete all data (start from 'git clone' state)"
	@echo " * runserver        - run runserver target of backend/Makefile - start django server"
	@echo " * deb              - build debian package"
	@echo "   * remove_deb     - remove installed Debian package"
	@echo "   * purge_deb      - purge installed Debian package"
	@echo "   * install_deb    - install previously built debian package"

devel: devel_backend devel_frontend
	@echo "Development environment is ready"


devel_backend:
	mkdir -p $(DATABASE_DIR)
	mkdir -p $(LOG_DIR)
	touch $(DJANGO_LOG_FILE)
	$(MAKE) -C backend devel VIRTUALENV=$(DEVEL_VIRTUALENV_DIR)


devel_frontend:
	$(MAKE) -C frontend build-devel

test_backend:
	$(MAKE) -C backend test

test_frontend:
	$(MAKE) -C frontend test

distclean:
	@echo
	@echo "Cleaning working directory"
	@echo
	git clean -fdx

runserver:
	$(MAKE) -C backend runserver VIRTUALENV=$(DEVEL_VIRTUALENV_DIR)

install:
	@echo
	@echo "Installing virtualenv"
	@echo
	mkdir -p $(INSTALL_VIRTUALENV)
	sudo mkdir -p $(DEPLOYMENT_ROOT)
ifneq ($(DOCKER_BUILD),true)
	# virtualenv is not relocatable - must install in target dir
	sudo mount -o bind $(INSTALL_ROOT) $(DEPLOYMENT_ROOT)
endif
	virtualenv -p python3 $(DEPLOYMENT_VIRTUALENV)
	$(DEPLOYMENT_VIRTUALENV)/bin/pip install -r backend/requirements.txt
	@echo
	@echo "Installing backend files"
	@echo
	mkdir -p $(INSTALL_ROOT)
	mkdir -p $(LOG_DIR)
ifneq ($(DOCKER_BUILD),true)
	# umount installation directory once no longer needed
	sudo umount -l $(DEPLOYMENT_ROOT)
else
	# under docker we don't need to be nice as the env is disposable
	mv $(DEPLOYMENT_VIRTUALENV) $(INSTALL_ROOT)
endif
	cp -r backend $(INSTALL_ROOT)
	cp -r bin $(INSTALL_ROOT)
	cp README.rst $(INSTALL_ROOT)
	cp -r etc ${DESTDIR}/
	cp -r ansible ${INSTALL_ROOT}
	@echo
	@echo "Backend installed in $(INSTALL_ROOT)"
	@echo

docker:
	docker build -t vpnathome .

deb:
	git clean -fdx
	debuild -e DOCKER_BUILD=$(DOCKER_BUILD) --no-lintian -i -uc -us -b

install_deb:
	sudo dpkg -i ../vpnathome*.deb

remove_deb:
	sudo dpkg --remove vpnathome

purge_deb:
	sudo dpkg --purge vpnathome
