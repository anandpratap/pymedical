#!/bin/bash
 
# (C) 2009 Guy Rutenberg
# Backup Django sites
FIRSTLINE=`head -n 1 .dir.log`
LASTLINE=`tail -n 1 .dir.log`
cp -r ${FIRSTLINE} ${LASTLINE}/