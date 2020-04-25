#!/usr/bin/env python3

from setuptools import find_packages, setup

# allow setup.py to be run from any path
# os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='vpnathome',
    packages=find_packages(where='backend'),
    package_dir={'vpnathome': 'backend/vpnathome'},
    version='2.1.1',
    include_package_data=True,
    package_data={'': ['*/*', '*/*/*', '*/*/*/*', '*/*/*/*/*']},  # nasty hack
    scripts=['scripts/init.sh', 'scripts/manage.py', 'scripts/run_daphne.sh', 'scripts/deploy_vpn.sh', 'scripts/inventory.sh'],
    license='GPL-3',
    description='1-click, self-hosted deployment of OpenVPN with DNS ad blocking sinkhole',
    url='https://github.com/ezaquarii/vpn-at-home',
    author='Chris Narkiewicz',
    author_email='hello@ezaquarii.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
