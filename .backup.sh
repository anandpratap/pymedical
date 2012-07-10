#!/bin/bash
 
# (C) 2009 Guy Rutenberg
# Backup Django sites
 
BACKUP_DIR="/home/maverick/Dropbox/Backup"
find ${BACKUP_DIR}* -type f -mtime +2 -exec rm '{}' '+'
 
# end of user configurable section
 
PROG=`basename "$0"`
echo $PROG
print_usage () {
    echo "USAGE: $0 [options] PROJ_ROOT"
    echo "Backup a Django project located in PROJ_ROOT"
}
 
print_help ()  {
    print_usage
    cat << EOF
 
Options:
    -h, --help          show this help message and exit
    --db-only           only backup the database
 
EOF
}
 
TEMP=`getopt -o h --long help,db-only -n "$PROG" -- "$@"`

 
eval set -- "$TEMP"
 
DB_ONLY="1" 
 
 
PROJECT_DIR="/home/maverick/Dropbox/projects/medical/"
 
# extract database variables from settings.py
cd "$PROJECT_DIR"
 
 
DB_ENGINE=`python -c "from settings import *; print DATABASES['default']['ENGINE']"`
if [ "$DB_ENGINE" != "django.db.backends.mysql" ]; then
 echo $DB_ENGINE
 echo "Only mysql databases are supported!">/dev/stderr
 exit 1
fi
 
DB_NAME=`python -c "from settings import *; print DATABASES['default']['NAME']"`
DB_USER=`python -c "from settings import *; print DATABASES['default']['USER']"`
DB_PASS=`python -c "from settings import *; print DATABASES['default']['PASSWORD']"`
DB_HOST=`python -c "from settings import *; print DATABASES['default']['HOST']"`
#TODO find how to use it
DB_PORT=`python -c "from settings import *; print DATABASES['default']['PORT']"`
 
# set optional parameters: host, port
HOST_ARGS=''
if [ -n "$DB_HOST" ]; then
 HOST_ARGS="--host $DB_HOST"
fi
 
PORT_ARGS=''
if [ -n "$DB_PORT" ]; then
 PORT_ARGS="--port $DB_HOST"
fi
 
SITE_DIR=`dirname "$PROJECT_DIR"`/`basename "$PROJECT_DIR"`
BACKUP_DIR=`dirname "$BACKUP_DIR"`/`basename "$BACKUP_DIR"`
 
echo -n "dumping database... "
DUMP_NAME=${DB_NAME}_$(date +%Y-%m-%d_%H-%M).sql
mysqldump --user=${DB_USER} --password=${DB_PASS} $HOST_ARGS \
 $PORT_ARGS --databases ${DB_NAME} > ${BACKUP_DIR}/${DUMP_NAME}
if (($?)); then
	echo "failed!"
	exit 1
fi
echo "done"
 
# PUT_TARBALL_FTP=""
# if [ "$DB_ONLY" -eq "0" ]; then
# 	echo -n "Creating tarball... "
# 	TAR_NAME=${SITE_DIR##*/}-$(date +%Y%m%d).tar.bz2
# 	tar -cjf ${BACKUP_DIR}/${SITE_DIR##*/}-$(date +%Y%m%d).tar.bz2 ${SITE_DIR}
# 	if (($?)); then
# 		echo "failed!"
# 		exit 2
# 	fi
# 	echo "done"
# 	PUT_TARBALL_FTP="put \"${BACKUP_DIR}/${TAR_NAME}\""
# fi
 
# echo -n "Uploading backup to FTP... "
 
# lftp -u ${FTP_USER},${FTP_PASS} ${FTP_HOST} <<EOF
# cd "${FTP_BACKUP_DIR}"
# put "${BACKUP_DIR}/${DUMP_NAME}"
# ${PUT_TARBALL_FTP}
 
# EOF
# if (($?)); then
# 	echo "failed!"
# 	exit 3
# fi
echo "done"