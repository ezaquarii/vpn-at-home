all:
	@echo "Welcome to OpenVPN@Home make system"
	@echo ""
	@echo "Available top-level targets:"
	@echo " * devel     - boostrap both projects for development"
	@echo " * runserver - run runserver target of backend/Makefile - start django server"
	@echo " * distclean - clean projects, delete all data (start from 'git clone' state)"

devel:
	$(MAKE) -C frontend build-devel
	$(MAKE) -C backend devel

distclean:
	$(MAKE) -C frontend distclean
	$(MAKE) -C backend distclean

runserver:
	$(MAKE) -C backend runserver
