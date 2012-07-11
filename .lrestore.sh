#!/bin/bash
 
# (C) 2009 Guy Rutenberg
# Backup Django sites
LASTLINE=`head -n 1 .dir.log` 
BACKUP_DIR=${LASTLINE}
cd ${BACKUP_DIR}
FILE_=`ls -tf1 | head -n1`
echo ${FILE_}
mysql --user=root --password=anandmedical990 medicaldata < \
    ${BACKUP_DIR}/${FILE_}
echo $(date +%Y-%m-%d_%H-%M)_${FILE_} >> ./log/restore.log
cd
