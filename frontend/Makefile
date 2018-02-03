YARN_TARGETS := (

all:
	@echo "Welcome to OpenVPN@Home make system - frontend sub-project"
	@echo "You need running node.js and yarn."
	@echo ""
	@echo "Available targets:"
	@echo " * start       - development build, output written to './dist', watching"
	@echo " * build-prod  - build production build, update backend files"
	@echo " * build-devel - development build, output written to './dist', but no watching"
	@echo " * install     - install packages from package.json"
	@echo " * distclean   - clean project, delete all data (start from 'git clone' state)"

start: install
	npm run-script start

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
