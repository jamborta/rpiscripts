#!/bin/sh
IPADDRESS=$(curl ip.alt.io)
if [ ! -z "${IPADDRESS}" -a "${IPADDRESS}" != $(cat ~/.current_ip) ];
then
echo "Your new IP address is ${IPADDRESS}" | mail -s "IP address change" jamborta@gmail.com
echo ${IPADDRESS} >|~/.current_ip
fi
