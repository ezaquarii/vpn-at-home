This software is no longer supported
====================================

I'm no longer maintaining this software.

VPN​@​Home - 2.1.1
==================

.. raw:: html

    <center>
        <a href="https://t.me/vpnathome"><img src="https://img.shields.io/badge/Telegram%20Chat-Online-success.svg"></a>
        <a href="./LICENCE.txt"><img src="https://img.shields.io/badge/license-GPL3-blue.svg"></a>
        <a href="https://www.vultr.com/?ref=7515725"><img src="https://img.shields.io/badge/use-vultr-brightgreen.svg"></a>
        <a href="https://www.patreon.com/ezaquarii"><img src="https://img.shields.io/badge/donate-patreon-brightgreen.svg"></a>
    </center>
    <center>
        <a href="https://vimeo.com/308879491"><img src="vimeo.png" width="512"></a>
    </center>

TL;DR
=====

What?
-----

1-click deployment of OpenVPN with DNS ad blocking sinkhole. Deploys to your favorite VPS machine.
Created with **Vue.js**, **Semantic UI** and **Django**. And with love, of course.

Where I can find packages
-------------------------

Ubuntu 20.04 users can use pre-built packages:

::

    $ sudo add-apt-repository ppa:ezaquarii/packages
    $ sudo apt-get update
    $ sudo apt-get install vpnathome
    $ firefox http://localhost:8000

Other distro dwellers must follow manual instructions found below.
Debian package building is automated, so there should be no trouble.

I do not maintain older Ubuntu versions as I don't run them.
There is a package for 18.04 that Launchpad built for me automatically,
but it is known to be broken.

What if I need halp!
--------------------

You can ask on `Telegram group chat <https://t.me/vpnathome>`_ or mail me (e-mail in git history).

Show me the screenshots
-----------------------

.. image:: home.png
   :width: 512
   :align: center

.. image:: deployment.png
   :width: 512
   :align: center

.. image:: settings.png
   :width: 512
   :align: center


Feedback and pull requests are welcome.

Legal mumbo-jumbo
=================

OpenVPN is a registered trademark of OpenVPN  Inc.
© 2002-2019 OpenVPN Inc.

This project is not endorsed by, sponsored or affiliated with OpenVPN Inc.

Brief
=====

Managing OpenVPN with PKI authentication is hard. Managing anything beyond hello-world using ``easy-rsa`` package
is a major issue - I could never maintain a config for more than a day. Other solutions are too *"enterprise"*
for a personal installation or were designed for a tin-foil hat, crypto maniacs hiding from NSA/GCHQ.

This app provides easy management console to keep OpenVPN configuration files in one place, provided in self-contained,
easily deployable, clickable package. It's not designed for security - it's meant just to be **good enough**.

And that works for me better than "no VPN at all".

Features:

#. 1-click deployment of OpenVPN server to your favorite VPS provider
#. DNS cache and ad blocking for VPN connected clients
#. OpenVPN clients management
#. Generation of self-contained ovpn profiles for servers and clients
#. Profiles can be sent by e-mail to owner or downloaded as files
#. Tested on Ubuntu 18.04 and OpenBSD 6.4 (Vultr VPS)

That's all folks.

.. note:: This is a work-in-progress app, hacked together during x-mas break to solve a specific need of mine.
          Feel free to submit PRs with improvements.

FAQ
===

**Why?**

To quickly deploy VPN server when I need it. I can spin VPS and deploy my own VPN any time, tear it down
when not used and not paying a monthly fee for all my devices.

I travel a lot and I need to have on-demand VPN when browsing stuff in hotels, airports, etc.

**Does it hide my ass? Can I haz torrentz?**

No. Do not use it to do any stupid things.

**Is the app secure?**

Since the app manages OpenVPN server deployment, it must have root access to the VPN
machine. There is no separate deployment agent (yet), as it would over-complicate things.
It is not wise to keep it facing the open internet, I guess, so please don't do it.

**So how to host it?**

Preferably on your internal network. Keep the server bound to *localhost* and connect to it
via SSH tunnel. This way you don't need to configure SSL certificate and a lot of security
headaches go away.

I use it installed on my private laptop, the same way I use CUPS (printer stuff, aka localhost-colon-six-three-one).

**Why it contains those tar.gz files in pypi directory?**

1. To enable offline builds;
2. To ship entire app in form of a source code, which is required by Launchpad;
3. To have reproducible builds, independent from external repositories;

Please read about
`npm package that broke the internet <https://duckduckgo.com/?q=npm+package+that+broke+the+internet>`_ to undestand
the downside of pulling your dependencies from 3rd party sources during build time.

**How to change server address after it is created?**

Use Django Admin panel to modify host field and re-deploy. All client configs must be re-deployed too.
You can try playing with DynDNS to work around it.

**Why Ansible? It's slow and weights 30MB.**

#. It does the job like a champ lifting tons of system complexity
#. Zero-effort deployment (no master nodes, etc)
#. Very easy to extend
#. I'd like to have more complex setup in the future and bash won't cut it

**Why not language X**?

I believe Python is optimal solution considering platform maturity, libraries quality and
skills proliferation. There is not much choice for the frontend.

Project structure
=================

The project is split into *backend*, *frontend*. and *ansible* scripts.

The backend is written in **Django** and **Django REST Framework**. The frontend is a **Vue.js** SPA application served by **Django**.
That division makes the build slightly more complicated, but provided *Makefiles* make it a breeze. It should just work.

**Ansible** is a set of scripts to deploy OpenVPN automatically either on localhost or remote machine.

Scripts located in **bin** are created either to automate and facilitate various tasks or provide a glue.
All scripts have internal documentation (or should have).

Installation
============

Prerequisites
-------------

#. Working Node.js installation (tested with 9.3.0)
#. Python 3 with virtualenv
#. GNU Make (or compatible)
#. Ansible (tested with 2.5.0, but no fancy functionality is used)
#. OpenVPN in ${PATH}
#. OpenSSL in ${PATH}
#. OpenSSH in ${PATH}
#. Internet connection (no off-line build possible)

Deployment
----------

For development
~~~~~~~~~~~~~~~

After cloning the repository, you can easily deploy the app for development:

::

    $ git clone https://github.com/ezaquarii/vpn-at-home
    $ cd vpn-at-home
    $ make install_dependencies  # apt-get only, other distros must do it manually
    ...follow instructions to install packages and Node.js...
    $ exec bash  # reload your shell to update $PATH and reload bashrc, so Node.js works, exec will replace the process
    $ make devel
    ... backend is bootstrapped ...
    ... frontend is bootstrapped ...
    $ make runserver

Open ``http://localhost:8001/`` and you should be able to log-in. Your app data
(config, ssh keys, etc) is stored in ``data`` directory in project's root.

If you completely mess up, delete data and run ``env/bin/init.sh`` to boostrap
the app again.

For production - Debian package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Package deployment is supported on *Ubuntu*. *Debian* should be supported, but I didn't test it there.

::

    $ make deb
    $ make install_deb

Open ``http://localhost:8000`` and follow on-boarding tutorial.

.. note:: Building ``deb`` package calls ``make distclean``, which will zap your development
          configuration. Build outside devel environment if you want to preserve your config.

The package needs virtually zero configuration:

- ``deb`` is self-deployable, as it contains entire virtualenv
- installs into ``/usr/lib/vpnathome`` (referred to as ``${ROOT}``)
- ``systemd`` service script ``vpnathome.service`` is installed and starts by default
- ``daphne`` runs on ``http://127.0.0.1:8000`` - bound to **localhost** only
- Application ``$HOME`` is ``/var/lib/vpnathome`` and all application data is stored there
- Bootstrapping script to automate app configuration in located in ``/var/lib/vpnathome/init.sh``

OpenVPN server deployment
~~~~~~~~~~~~~~~~~~~~~~~~~

Once the app is up and running, you can log in as admin (using credentials set during bootstrapping phase) and
create your server.

After a server is configured, you can deploy it using provided **Ansible** scripts by clicking ``Deploy``
option in server list. Beware that *Ansible* will modify the target system!

#. required packages will be installed
#. firewall rules will be altered
#. IPv4 forwarding will be enabled

If the app fails to log into a target system, make sure you have the correct SSH keys uploaded to the server
(check out ``data/ssh`` directory).

Configuration
-------------

If ``make devel`` was run, the app is up and running in development mode with default development
configuration:

- Admin login is *admin@locahost*
- Admin password is *admin1234*
- Database is located in ``${PROJECT_ROOT}/data/db/db.sqlite3``
- Settings have ``development`` flag set to true ``true`` causing frontend code to be taken from ``frontend`` project

Activate Python virtualenv when before running ``manage.py``!
To set new superuser, use ``${PROJECT_ROOT}/env/bin/manage.py set_admin <email> <pass>`` command.

App config
~~~~~~~~~~

Configuration is loaded from ``settings.json`` located in ``data`` directory in the current working directory.

The settings file is generated during bootstrap stage (``init.sh``), so there is no need to generate it
manually. However, should you need to generate the script during development, you can do it with a supplied
Django management command:

::

    $ source ${PROJECT_ROOT}/env/bin/activate  # activate Python virtual environment first!
    $ ${PROJECT_ROOT}/env/bin/manage.py configure --help

Once the file is generated, you must review and accept it by flipping the ``configured`` flag.

Alternative way is to run ``init.sh``:

::

    $ ${PROJECT_ROOT}/env/bin/init.sh [--no-smtp]

Just follow the wizard. It will accept the configuration for you, so there is no need to flip the flag.

.. note:: ``settings.json`` is excluded from Git repository, so you can safely put your real e-mail credentials there
          during development.

OpenVPN config
~~~~~~~~~~~~~~

OpenVPN configuration is generated from templates in ``vpnathome.apps.openvpn.templates``. If the default
configuration doesn't suit your needs, you can alter templates directly there.

There is no frontend config editor, although I was thinking about it.

Client connection
-----------------

Obtaining client config
~~~~~~~~~~~~~~~~~~~~~~~

VPN config files can be send to e-mail account of a user that created a config or downloaded.
Once downloaded, the config file (OVPN) can be used directly with OpenVPN client.

DNS check
~~~~~~~~~

If server was deployed with DNS cache enabled, DNS is forwarded to connecting client.
Depending on your network this might be slower or faster than popular DNS servers or DNS of your ISP.

To verify if your queries are forwarded to VPN DNS:

::

    ping gateway.vpnathome
    PING gateway.vpnathome (172.30.0.1) 56(84) bytes of data.
    64 bytes from _gateway (172.30.0.1): icmp_seq=1 ttl=255 time=46.5 ms
    64 bytes from _gateway (172.30.0.1): icmp_seq=2 ttl=255 time=48.7 ms

where ``172.30.0.1`` will be your choosen VPN gateway IP. Check ``systemd-resolve --status`` if DNS servers are
properly pushed.

Development
===========

Want to jump in? Fantastic.

I made it as easy to start development as possible. Top-level project directory contains 2 subprojects:
``backend`` and ``frontend``.

Top-level ``Makefile`` delegates targets to sub-projects and is provided for convenience. Once ``make devel`` is
done, you can work inside individual subproject with your favourite IDE.

I personally use *JetBrains WebStorm* and *PyCharm*, but you can use whatever you want.
IDE files are not even in the repo.

Backend subproject
------------------

This is the **Django** app. Mostly REST API + single frontend serving view.
App modules have brief documentation inside ``__init__.py``. Docs are kept up-to-date, as I strongly
believe in code documentation.

Provided ``Makefile``'s default target displays help:

::

    $ make
    Welcome to VPN@Home make system
    
    Available top-level targets:
     * install_dependencies - convenient shortcut to install build dependencies (packages and node.js)
     * devel                - bootstrap both projects for development
       * devel_backend      - bootstrap backend for development (dependency of devel)
       * devel_frontend     - bootstrap frontend for development (dependency of devel)
     * distclean            - clean projects, delete all data (start from 'git clone' state)
     * runserver            - run development server (manage.py runserver)
     * deb                  - build debian package
       * remove_deb         - remove installed Debian package
       * purge_deb          - purge installed Debian package
       * install_deb        - install previously built debian package

In development mode, frontend files are stored outside of this project, in ``frontend`` subproject. **Django** app
will pick static and templates from frontend build directory.

When development mode is off, frontend resources are taken from ``vpnathome.apps.frontend`` app.

**Django Debug Toolbar** is provided by default, should you need to check which templates are picked up.

Frontend subproject
-------------------

Frontend sub-project contains **Vue.js** SPA served by **Django**. By default **Django** app will serve
stable, production version of the frontend app directly.

Provided ``Makefile``'s default target displays help:

::

    $ cd frontend
    $ make
    Welcome to VPN@Home make system - frontend sub-project
    You need running node.js and npm.

    Available targets:
     * build-prod  - build production build; backend project is NOT updated
     * build-devel - watch and make development build on change; output is written to './dist'
     * install     - install packages from package.json
     * distclean   - clean project, delete all data (start from 'git clone' state)

To start development of frontend code, you must first switch backend into development mode, by modifying ``data/settings.json``:

::

    {
        ...
        "configured": true,
        "development": true,
        "debug_toolbar_enabled": true,
        ...

Don't forget to restart the app. Once development mode is enabled, **Django** will load frontend from ``frontend/dist``
instead of ``vpnathome.apps.frontend``. You can verify this by inspecting site title - it should say
*VPN@Home <version> - development*. You can also use **Django Debug Toolbar** to troubleshoot the configuration.

**Django** injects some initial state via ``<script>...</script>`` tag. See ``index.html`` and ``vpnathome.apps.frontent.views`` for
details.

Licence
=======

GNU GPL v3.

Known issues
============

I left this as the last point, hoping not to scare anybody.

 * frontend has 0% test coverage :o)
 * security is not a major concern for this app, I'm not running a CA company
 * no real user management - I rely on Django Admin panel for it
 * not tested on Windows, as I don't touch it even with a 10-foot stick, in rubber gloves - patches are welcome, however
 * no cert revocation (yet)
