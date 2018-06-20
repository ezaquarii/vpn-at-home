all:
	@echo "Welcome to OpenVPN@Home make system - frontend sub-project"
	@echo "You need running node.js and npm."
	@echo ""
	@echo "Available targets:"
	@echo " * build-prod  - build production build; backend project is NOT updated"
	@echo " * build-devel - watch and make development build on change; output written to './dist'"
	@echo " * install     - install packages from package.json"
	@echo " * distclean   - clean project, delete all data (start from 'git clone' state)"

build-prod: install
	npm run-script build-prod

build-devel: install
	npm run-script build-devel

install:
	npm install

lint:
	npm run-script lint

distclean:
	rm -rf node_modules
	rm -rf dist
	rm -f package-lock.json
	@echo "All frontend build data deleted."
