#!/bin/sh
sleep 3
NOW=$(date +"%Y%m%d_%H%M%S")
name="$NOW""_$1"
zip -m /tmp/$name.zip /tmp/motion/*
/home/pi/dropbox_uploader/dropbox_uploader.sh upload /tmp/$name.zip
rm /tmp/$name.zip 
