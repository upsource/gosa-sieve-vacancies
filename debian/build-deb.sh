#!/bin/bash
set -e;
BASE=`dirname "$(readlink -f "$0")"`
VERSION=0.1.$1
TARGET="/out"

echo "cleanup ${BASE}/${TARGET}" ;
test ! -d "${BASE}/${TARGET}" || rm -rf "${BASE}/${TARGET}";
mkdir ${BASE}/${TARGET};
cd ${BASE}/${TARGET}

fpm -s dir --log info -t deb \
-m "upSource GmbH <info@upsource.de>" \
-n "gosa-sieve-vacancies" \
-v ${VERSION} \
--depends python-ldap \
--vendor "upSource GmbH" \
--license MIT \
--category net \
--url https://www.upsource.de \
--description "creates sieve files for vacancy reply messages from open-ldap in gosa scheme" \
--deb-user "vmail" \
--deb-group "vmail" \
--config-files /etc/gosa-sieve-vacancies/sync-vacancies.conf.json \
--config-files /etc/gosa-sieve-vacancies/sieve-template.tpl \
--after-install ${BASE}/postinst.sh \
--after-upgrade ${BASE}/postinst.sh \
${BASE}/../sync-vacancies.conf.json=/etc/gosa-sieve-vacancies/sync-vacancies.conf.json \
${BASE}/../sieve-template.tpl=/etc/gosa-sieve-vacancies/sieve-template.tpl \
${BASE}/../sync-vacancies.py=/opt/bin/sync-vacancies.py \
${BASE}/gosa-sieve-vacancies.cron=/etc/cron.d/gosa-sieve-vacancies \
${BASE}/91-vacation-sieve.conf=/etc/dovecot/conf.d/91-vacation-sieve.conf
