#!/usr/bin/env sh

ROOT=`realpath $(dirname "$0")/`

cd ${ROOT}
. ../env/bin/activate
setsid uwsgi $* uwsgi.ini
