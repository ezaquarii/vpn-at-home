SHELL := /bin/bash
PATH := $(PWD)/bin:$(PATH)
ENV := env
PYTHON := $(ENV)/bin/python3

.PHONY: devel devel_backend distclean runserver install install_backend install_virtualenv install_etc deb install_deb uninstall_deb

all:
	@echo "Welcome to VPN@Home make system"
	@echo
	@echo "Available top-level targets:"
	@echo " * install_dependencies - convenient shortcut to install build dependencies (packages and node.js)"
	@echo " * devel                - bootstrap both projects for development"
	@echo "   * devel_backend      - bootstrap backend for development (dependency of devel)"
	@echo "   * devel_frontend     - bootstrap frontend for development (dependency of devel)"
	@echo " * distclean            - clean projects, delete all data (start from 'git clone' state)"
	@echo " * runserver            - run development server (manage.py runserver)"
	@echo " * deb                  - build debian package"
	@echo "   * remove_deb         - remove installed Debian package"
	@echo "   * purge_deb          - purge installed Debian package"
	@echo "   * install_deb        - install previously built debian package"


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
	rm -rf .cache
	rm -rf .idea
	rm -rf .pydistutils.cfg
	rm -rf build/
	rm -rf debian/.debhelper/
	rm -rf debian/debhelper-build-stamp
	rm -rf debian/files
	rm -rf debian/vpnathome.postinst.debhelper
	rm -rf debian/vpnathome.postrm.debhelper
	rm -rf debian/vpnathome.prerm.debhelper
	rm -rf debian/vpnathome.substvars
	rm -rf debian/vpnathome/
	rm -rf dist/
	rm -rf env/
	rm -rf vpnathome.egg-info/

env:
	python3 -m venv env
	$(PYTHON) env/bin/pip install pypi/wheel*tar.gz
	$(PYTHON) env/bin/pip install --no-cache --no-index --find-links=pypi -r requirements.txt
	ln -s $(CURDIR)/backend/vpnathome "`find env -name site-packages`"
	ln -sr scripts/manage.py env/bin/
	ln -sr scripts/deploy_vpn.sh env/bin/
	ln -sr scripts/inventory.sh env/bin/
	ln -sr scripts/init.sh env/bin/

install_dependencies:
	@echo Installing packaged dependencies. You may be asked to type sudo passoword. It will
	@echo use apt-get package manager to install dependencies from trusted, system repository.
	@sudo apt install \
		debhelper \
		make \
		python3 \
		python3-pip \
		python3-dev \
		python3-wheel \
		python3-venv \
		devscripts \
		debhelper \
		dialog \
		sudo \
		libffi-dev \
		libssl-dev \
		openvpn \
		openssh-client \
		ansible

	@echo Since packaged Node.js is hopelessly outdated, it is necessary to install it using NVM.
	@echo 'This step will install NVM in your $$HOME and will modify your .bashrc startup script!!!'
	@echo If you are not sure about this step, please abort and read about NVM and Node.js intallation.
	@echo You can safely re-run this make target to finish it later.
	@echo
	@echo Press Enter to continue or Ctrl-C to abort.

	@read

	@echo Updating NVM installation in your home directory.
	@mkdir -p $(HOME)/.nvm/  # in case you have NVM_DIR set, installation script will fail without existing dir
	@bash ./scripts/install_node_nvm_0.34.0.sh

	@echo Installing recommended Node.js version.
	@source $(HOME)/.nvm/nvm.sh && nvm install 10.15.3
	@source $(HOME)/.nvm/nvm.sh && nvm use 10.15.3

	@echo
	@echo Dependencies required for development are installed.
	@echo Reload your shell to use NVM-installed Node.js.
	@echo After that, you can make devel to bootstrap your development environment.
	@echo Enjoy!

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

.PHONY: build
build:
	(echo '[easy_install]'; \
	 echo 'find_links = file://$(PWD)/pypi/') \
		>$(PWD)/.pydistutils.cfg
	python3 -m venv env
	HOME=$(PWD) $(PYTHON) env/bin/pip install pypi/wheel*tar.gz
	HOME=$(PWD) $(PYTHON) env/bin/pip install --no-cache --no-index --find-links=pypi -r requirements.txt
	$(PYTHON) setup.py install

build.stamp: build
install: build.stamp
	$(CURDIR)/install_venv.sh env ${DESTDIR}/
