#!/bin/bash
# set -e

if [ "$1" != "FULL" ]
then
    opt="5 minutes ago"
else
    opt="7 days ago"
fi

echo "Finding bad actors"
time journalctl -u sshd --since="${opt}" | fgrep Failed | fgrep from | egrep -o 'from [0-9\.]*' >> .ip.list.txt
cat .ip.list.txt | sort -u | cut -f2 -d' ' > .ip.sortu.list.txt

echo "Bouncing firewall"
systemctl restart firewalld

echo "Adding bad actors"
for IP in `cat .ip.sortu.list.txt`
do
    echo "  adding $IP"
    iptables -w 60 -A IN_public_deny -s $IP -j DROP 2>/dev/null
done


MY_IP=`cat /root/myip.txt`
echo "Removing my ip $MY_IP"
iptables -D INPUT -s $MY_IP -j DROP 2>/dev/null
iptables -D IN_public_deny -s $MY_IP -j DROP 2>/dev/null

echo "Added this many bad actors"
wc -l .ip.sortu.list.txt

mv .ip.list.txt .ip.list.txt.bak
sort -u .ip.list.txt.bak | fgrep -v 'from from' > .ip.list.txt
rm .ip.list.txt.bak
