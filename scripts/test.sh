#!/bin/bash

emerge --update --newuse --deep --with-bdeps=y @world --keep-going
emerge --update --newuse --deep --with-bdeps=y @world --keep-going

echo "world build one" > timeslog
date >> timeslog
emerge  --keep-going --emptytree @world 2>&1 | tee worldbuild.log
date >> timeslog

echo -e "\n\n\n" >> timeslog

echo "world build two" >> timeslog
date >> timeslog
emerge  --keep-going --emptytree @world 2>&1 | tee worldbuild.two.log
date >> timeslog

emerge --update --newuse --deep --with-bdeps=y @world  --keep-going
emerge --update --newuse --deep --with-bdeps=y @world  --keep-going
sync
sleep 5
systemctl suspend
