#!usr/bin/env bash

su
apt-get update && apt-get upgrade
apt-get install wget python3 python3-pip nmap net-tools xdotool xfce4-terminal git

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && apt install ./google-chrome-stable_current_amd64.deb

git clone https://github.com/lewenhagen/maxlew_videosystem.git

cd ~/maxlew_videosystem && pip3 install -r requirements.txt
