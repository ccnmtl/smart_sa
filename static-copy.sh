#!/bin/bash

ADMIN_PORT=""
ADMIN_DOMAIN="smartsa.ccnmtl.columbia.edu"
#ADMIN_PORT=":8000" #debug
#ADMIN_DOMAIN="localhost"
ADMIN_URL="http://${ADMIN_DOMAIN}${ADMIN_PORT}"


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

find .  -type f |grep -v svn |grep -v /accounts/ |grep -v /selenium/ |grep -v /mochikit/scripts/ |grep -v /mochikit/tests/ |grep -v /mochikit/doc/ |grep -v /accounts/ |grep -v DS_Store |grep -v /mochikit/examples/ |grep -v ~$|grep -v \.zip |sed -e 's/^\.//g' >site_media/cache-manifest.txt

cp site_media/cache-manifest.txt ../../media/

cd ..
../windows-link.py $DOWNLOAD_DIR > ${DOWNLOAD_DIR}/SMART.bat


echo $FAKE_HEXKEY
echo $HEXKEY
echo $FAKE_HEXKEY_IV
echo $HEXKEY_IV


perl -pi -e "s/${FAKE_HEXKEY}/${HEXKEY}/" ${DOWNLOAD_DIR}/masivukeni_admin_data.html
perl -pi -e "s/${FAKE_HEXKEY_IV}/${HEXKEY_IV}/" ${DOWNLOAD_DIR}/masivukeni_admin_data.html

zip -r ${DOWNLOAD_DIR}.zip ${DOWNLOAD_DIR} -x \*.svn\*
