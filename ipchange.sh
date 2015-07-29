#!/bin/sh
IPADDRESS=$(curl ip.alt.io)
LEN=$(echo ${#IPADDRESS})

if [ ! -z "${IPADDRESS}" -a $LEN -lt 15 -a "${IPADDRESS}" != $(cat ~/.current_ip) ];
then
echo "Your new IP address is ${IPADDRESS}" | mail -s "IP address change" jamborta@gmail.com
echo ${IPADDRESS} >|~/.current_ip
else
echo "String is too long: $IPADDRESS, size: $LEN"
fi
