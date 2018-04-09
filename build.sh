#!/bin/sh
#

TARGET="out"
TEMPLATE="euca-me-template.json"
CLOUDCONFIG="cloud-config.yaml"

[ ! -e "${TARGET}" ] || rm -rvf "${TARGET}"
mkdir -pv "${TARGET}"

echo "Building cloud config"
sed 's/^/        /' "euca-me.py" > "${TARGET}/euca-me.py"
sed 's/^/        /' "httpd.conf" > "${TARGET}/httpd.conf"
sed 's/^/        /' "pdns.conf"  > "${TARGET}/pdns.conf"
cp "${CLOUDCONFIG}" "${TARGET}"
sed --in-place "/@@EUCA-ME_PY@@/r ${TARGET}/euca-me.py"  "${TARGET}/${CLOUDCONFIG}"
sed --in-place "s/@@EUCA-ME_PY@@//"                      "${TARGET}/${CLOUDCONFIG}"
sed --in-place "/@@HTTPD_CONF@@/r ${TARGET}/httpd.conf"  "${TARGET}/${CLOUDCONFIG}"
sed --in-place "s/@@HTTPD_CONF@@//"                      "${TARGET}/${CLOUDCONFIG}"
sed --in-place "/@@PDNS_CONF@@/r ${TARGET}/pdns.conf"    "${TARGET}/${CLOUDCONFIG}"
sed --in-place "s/@@PDNS_CONF@@//"                       "${TARGET}/${CLOUDCONFIG}"

echo "Building cloudformation template"
pipenv run python template.py > "${TARGET}/${TEMPLATE}"

ls -1 out