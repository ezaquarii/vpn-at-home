DEVEL_VIRTUALENV_DIR=$(CURDIR)/env
DATABASE_DIR=$(CURDIR)/db
CONFIG_FILE=$(CURDIR)/config.json

INSTALL_ROOT=$(DESTDIR)/srv/openvpnathome
PIP=$(VIRTUALENV)/bin/pip
PYTHON=$(VIRTUALENV)/bin/python3

all:
	@echo "Welcome to OpenVPN@Home make system"
	@echo ""
	@echo "Available top-level targets:"
	@echo " * devel      - boostrap both projects for development"
	@echo " * distclean  - clean projects, delete all data (start from 'git clone' state)"
	@echo " * runserver  - run runserver target of backend/Makefile - start django server"

devel:
	mkdir -p $(DATABASE_DIR)
	$(MAKE) -C backend devel VIRTUALENV=$(DEVEL_VIRTUALENV_DIR)
	$(MAKE) -C frontend build-devel
	@echo "Development environment is ready"

distclean:
	$(MAKE) -C frontend distclean
	rm -rf $(DEVEL_VIRTUALENV_DIR)
	rm -rf $(DATABASE_DIR)
	rm -rf $(CONFIG_FILE)

runserver:
	$(MAKE) -C backend runserver

#install: $(VIRTUALENV)
#	mkdir -p $(INSTALL_ROOT)
#	cp -r $(VIRTUALENV) $(INSTALL_ROOT)
#	cp -r backend $(INSTALL_ROOT)
#
#$(VIRTUALENV):
#	mkdir -p $(VIRTUALENV)
#	virtualenv -p python3 $(VIRTUALENV)
#	$(PIP) install -r backend/requirements.txt
#
#build_deb:
#	rm -rf debian/openvpnathome
#	rm -rf debian/source
#	debuild --no-lintian -i -uc -us -b
