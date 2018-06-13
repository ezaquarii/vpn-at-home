DEVEL_VIRTUALENV_DIR=$(CURDIR)/env
DATABASE_DIR=$(CURDIR)/db
CONFIG_FILE=$(CURDIR)/config.json

INSTALL_ROOT=$(DESTDIR)/srv/openvpnathome
INSTALL_VIRTUALENV=$(INSTALL_ROOT)/env
DEPLOYMENT_ROOT=/srv/openvpnathome
DEPLOYMENT_VIRTUALENV=$(DEPLOYMENT_ROOT)/env/

.PHONY: devel distclean runserver install install_backend install_virtualenv install_etc deb install_deb uninstall_deb

all:
	@echo "Welcome to OpenVPN@Home make system"
	@echo ""
	@echo "Available top-level targets:"
	@echo " * devel      - boostrap both projects for development"
	@echo " * distclean  - clean projects, delete all data (start from 'git clone' state)"
	@echo " * runserver  - run runserver target of backend/Makefile - start django server"


devel: devel_backend devel_frontend
	@echo "Development environment is ready"
	@echo "Run backend/manage.py bootstrap to initialize the database


devel_backend:
	mkdir -p $(DATABASE_DIR)
	$(MAKE) -C backend devel VIRTUALENV=$(DEVEL_VIRTUALENV_DIR)


devel_frontend:
	$(MAKE) -C frontend build-devel


distclean:
	@echo
	@echo "Cleaning working directory"
	@echo
	#$(MAKE) -C frontend distclean
	#rm -rf $(DEVEL_VIRTUALENV_DIR)
	#rm -rf $(DATABASE_DIR)
	#rm -rf $(CONFIG_FILE)


runserver:
	$(MAKE) -C backend runserver


install: install_virtualenv install_backend install_etc
	@echo "Backend installed in $(TARGET_ROOT)"


install_virtualenv:
	@echo
	@echo "Installing virtualenv"
	@echo
	mkdir -p $(INSTALL_VIRTUALENV)
	mkdir -p $(DEPLOYMENT_ROOT)
	sudo mount -o bind $(INSTALL_ROOT) $(DEPLOYMENT_ROOT)
	virtualenv -p python3 $(DEPLOYMENT_VIRTUALENV)
	$(DEPLOYMENT_VIRTUALENV)/bin/pip install -r backend/requirements.txt
	sudo umount -l $(DEPLOYMENT_ROOT)


install_backend:
	@echo
	@echo "Installing backend files"
	@echo
	mkdir -p $(INSTALL_ROOT)
	cp -r static $(INSTALL_ROOT)
	cp -r backend $(INSTALL_ROOT)
	cp -r bin $(INSTALL_ROOT)
	cp README.rst $(INSTALL_ROOT)


install_etc:
	cp -r etc ${DESTDIR}/

deb:
	rm -rf debian/openvpnathome
	rm -rf debian/source
	debuild --no-lintian -i -uc -us -b

install_deb:
	sudo dpkg -i ../openvpnathome*.deb

uninstall_deb:
	sudo dpkg --remove openvpnathome
