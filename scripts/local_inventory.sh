#!/usr/bin/env bash
#
# Ansible inventory script for local deployment. You should not call
# this script manually.
#

. $(dirname $0)/common.sh

"${PYTHON}" "${MANAGE}" ansible_inventory --local $@
