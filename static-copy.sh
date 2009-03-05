#!/bin/bash

ADMIN_DOMAIN="smartsa.ccnmtl.columbia.edu"
ADMIN_URL="http://${ADMIN_DOMAIN}"

STAMP=`date +%Y%m%d_%H%M`
DOWNLOAD_PATH="snapshots"
#DOWNLOAD_DIR="smartsa_$STAMP"
DOWNLOAD_DIR="Masivukeni"

FAKE_HEXKEY=`python -c'from settings_shared import *;print FAKE_INTERVENTION_BACKUP_HEXKEY'`
FAKE_HEXKEY_IV=`python -c'from settings_shared import *;print FAKE_INTERVENTION_BACKUP_IV'`

HEXKEY=`python -c'from settings_production import *;print INTERVENTION_BACKUP_HEXKEY'`
HEXKEY_IV=`python -c'from settings_production import *;print INTERVENTION_BACKUP_IV'`

rm -rf $DOWNLOAD_PATH/*
mkdir -p $DOWNLOAD_PATH/$DOWNLOAD_DIR/multimedia/
cp -r --dereference media $DOWNLOAD_PATH/$DOWNLOAD_DIR/site_media

cd $DOWNLOAD_PATH/$DOWNLOAD_DIR

wget --quiet \
    --no-clobber \
    --no-host-directories  \
    --exclude-directories="admin,intervention_admin" \
    --convert-links \
    --page-requisites \
    --html-extension \
    --recursive --level=50 \
    --domains="${ADMIN_DOMAIN}" \
    $ADMIN_URL

cd ..
../windows-link.py $DOWNLOAD_DIR > ${DOWNLOAD_DIR}/SMART.bat


echo $FAKE_HEXKEY
echo $HEXKEY
echo $FAKE_HEXKEY_IV
echo $HEXKEY_IV


perl -pi -e "s/${FAKE_HEXKEY}/${HEXKEY}/" ${DOWNLOAD_DIR}/masivukeni_admin_data.html
perl -pi -e "s/${FAKE_HEXKEY_IV}/${HEXKEY_IV}/" ${DOWNLOAD_DIR}/masivukeni_admin_data.html

zip -r ${DOWNLOAD_DIR}.zip ${DOWNLOAD_DIR} -x \*.svn\*
