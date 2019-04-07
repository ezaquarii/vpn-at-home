#!/usr/bin/env bash
#
# Ansible inventory script for local deployment. You should not call
# this script manually.
#

export BIN_DIR=$(readlink -f $(dirname "$0"))
source ${BIN_DIR}/activate

manage.py ansible_inventory $@
