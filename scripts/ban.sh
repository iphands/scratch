#!/bin/bash
set -e

if [ "$1" != "FULL" ]
then
    opt="5 minutes ago"
else
    opt="7 days ago"
fi

LIST_FILE="/root/.ip.list.txt"
LIST_FILE_RAW="${LIST_FILE}.raw"
LIST_FILE_TMP="${LIST_FILE}.bak"

OLD_COUNT="`fgrep from $LIST_FILE_RAW 2>/dev/null | wc -l 2>/dev/null`"

echo "Finding bad actors"
time journalctl -u sshd --since="${opt}" | fgrep Failed | fgrep from | egrep -o 'from [0-9\.]*' >> $LIST_FILE_RAW
cat $LIST_FILE_RAW | sort -u | cut -f2 -d' ' > $LIST_FILE

echo "Bouncing firewall"
systemctl restart firewalld
sleep 0.750

echo "Adding bad actors"
for IP in `cat $LIST_FILE`
do
    echo "  adding $IP"
    iptables -w 60 -A IN_public_deny -s $IP -j REJECT
done

MY_IP=`cat /root/myip.txt`
echo "Removing my ip $MY_IP"
iptables -D INPUT -s $MY_IP -j DROP 2>/dev/null || true
iptables -D IN_public_deny -s $MY_IP -j DROP 2>/dev/null || true

echo "Old count:"
echo $OLD_COUNT

echo "New count:"
wc -l $LIST_FILE | awk '{print $1}'

cp $LIST_FILE_RAW $LIST_FILE_TMP
sort -u $LIST_FILE_TMP | fgrep -v 'from from' > $LIST_FILE_RAW
rm $LIST_FILE_TMP
