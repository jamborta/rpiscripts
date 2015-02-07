#!/bin/bash
service=plotly-raspi-stream.py

if (( $(ps -ef | grep -v grep | grep $service | wc -l) > 0 ))
then
  echo "$service is running!!!"
else
  nohup python /home/pi/rpiscripts/plotly-raspi-stream.py $1 &>> /home/pi/rpiscripts/sensor.log &
fi
