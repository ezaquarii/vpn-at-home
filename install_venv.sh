#!/bin/sh

set -e

if [ -z $1 ] || [ -z $2 ]; then
  echo Usage: $0 src dest
  exit 1
fi

SRC=$(realpath $1)
DEST=$(realpath $2)

SRC_VENV_ROOT="${SRC}"
SRC_VENV_PYTHON="${SRC}/bin/python3"
SRC_VENV_PYTHON_ESC="$(echo ${SRC_VENV_PYTHON} | sed 's/\//\\\//g')"
SRC_VENV_SHEBANG="#!${SRC_VENV_PYTHON}"
SRC_VENV_SHEBANG_ESC="$(echo ${SRC_VENV_SHEBANG} | sed 's/\//\\\//g')"

PACKAGE_VENV="/usr/lib/vpnathome/venv"
PACKAGE_VENV_ESC="$(echo ${PACKAGE_VENV} | sed 's/\//\\\//g')"
PACKAGE_VENV_BIN="${PACKAGE_VENV}/bin"
PACKAGE_VENV_PYTHON="${PACKAGE_VENV_BIN}/python3"
PACKAGE_VENV_PYTHON_ESC="$(echo ${PACKAGE_VENV_PYTHON} | sed 's/\//\\\//g')"
PACKAGE_VENV_SHEBANG="#!${PACKAGE_VENV_PYTHON}"
PACKAGE_VENV_SHEBANG_ESC="$(echo ${PACKAGE_VENV_SHEBANG} | sed 's/\//\\\//g')"

DEST_VENV="${DEST}/${PACKAGE_VENV}"
DEST_VENV_BIN="${DEST}/${PACKAGE_VENV_BIN}"
DEST_VENV_PYTHON="${DEST}/${PACKAGE_VENV_PYTHON}"

echo "Source venv root:        [${SRC_VENV_ROOT}]"
echo "Source venv python:      [${SRC_VENV_PYTHON}]"
echo "Source venv python esc:  [${SRC_VENV_PYTHON_ESC}]"
echo "Source venv shebang:     [${SRC_VENV_SHEBANG}]"
echo "Source venv shebang esc: [${SRC_VENV_SHEBANG_ESC}]"
echo
echo "Package venv              [${PACKAGE_VENV}]"
echo "Package venv esc          [${PACKAGE_VENV_ESC}]"
echo "Package venv bin          [${PACKAGE_VENV_BIN}]"
echo "Package venv python       [${PACKAGE_VENV_PYTHON}]"
echo "Package venv shebang:     [${PACKAGE_VENV_SHEBANG}]"
echo "Package venv shebang esc: [${PACKAGE_VENV_SHEBANG_ESC}]"
echo
echo "Dest venv        [${DEST_VENV}]"
echo "Dest venv bin    [${DEST_VENV_BIN}]"
echo "Dest venv python [${DEST_VENV_PYTHON}]"

IFS="
"


rm -rf ${DEST}
mkdir -p "$(dirname ${DEST_VENV})"
cp -r "${SRC_VENV_ROOT}" "${DEST_VENV}"

SED_SHEBANG_SCRIPT="s/^#!.*python3.*/${PACKAGE_VENV_SHEBANG_ESC}/g"
echo "Patch script: [${SED_SHEBANG_SCRIPT}]"
for f in $(find "${DEST_VENV_BIN}" -type f -executable); do
  echo "Patching $f"
  echo ${SED_SHEBANG_SCRIPT} | sed -f - -i $f
done

SED_ACTIVATION_SCRIPT="s/VIRTUAL_ENV=.*/VIRTUAL_ENV=\"${PACKAGE_VENV_ESC}\"/g"
echo "Patching activation script"
echo ${SED_ACTIVATION_SCRIPT} | sed -f - -i "${DEST_VENV_BIN}/activate"

echo "Remove other activation scripts"
rm -fv "${DEST_VENV_BIN}/activate.csh"
rm -fv "${DEST_VENV_BIN}/activate.fish"
rm -fv "${DEST_VENV_BIN}/Activate.ps1"