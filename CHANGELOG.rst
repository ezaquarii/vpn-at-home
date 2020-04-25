Changelog
=========

2019-04-25 - release 2.1.1
--------------------------

 * Removed dependency on dh_virtualenv
 * Package compiledon Ubuntu 20.04

2019-12-27 - release 2.1.0
--------------------------

* Increased certificate key size to 4096
* Certificate validity time can be set on creation
* Upgraded Django to 2.2.9

2019-08-18 - release 2.0.3
--------------------------

* Updated dependencies to newest versions

2019-04-07 - release 2.0.2
--------------------------

* Fixed make runserver target
* Added install_dependencies Makefile target
* Updated hopelessly outdated README
* Removed unmaintained docker files (broken anyway)

2019-04-06 - release 2.0.1
--------------------------

* Fixed broken make devel deployment

2019-01-05 - release 2.0.0
--------------------------

* Huge refactoring
* Migrate off virtualenv to venv
* Use dh_virtualenv debhelper to create deb

2018-12-16 - release 1.8.0
--------------------------

* Change app name to VPN@Home

2018-12-15 - release 1.7.0
--------------------------

* Removed broken configurable mail backend
* Support deployment on OpenBSD
* Support multiple servers
* Support server deletion

2018-12-08 - release 1.6.0
--------------------------

* Docker support
* Fixed 500 error when accessing app before bootstrapping

2018-11-21 - release 1.5.0
--------------------------

* daphne replaced uwsgi server
* 1-click server deployment
* FAQ
* jQuery is no longer downloaded from internet
* Automatic VPN deployment using Ansible script

2018-06-20 - release 1.4.0
--------------------------

* frontend rewritten in Vue.js
* debian package!
* onboarding tutorial

2018-03-03 - release 1.3.0
--------------------------

* squashed migrations to avoid issues on SQLite3
* fixed issue with broken Semantic-UI package (dialogs were misplaced)
* migrated django-x509 to v0.4

2018-02-24 - relase 1.2.0
--------------------------

* frontend update

2018-02-03 - relase 1.1.0
--------------------------

* added VPN carrier protocol option

2018-01-07 - release 1.0.0
--------------------------

* initial release
