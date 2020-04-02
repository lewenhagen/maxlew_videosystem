#!/usr/bin/env sh

# Needed software
#
# google chrome
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo apt install ./google-chrome-stable_current_amd64.deb
#
# xdotool
# sudo apt-get install xdotool

# Command to find connected Axis cameras
# nmap -sP $(ifconfig | grep eno1 -a1 | tail -1 | sed -En 's/inet.([0-9]{3}.*)\s\snetmask.*/\1/p' | cut -d"." -f1-3 | xargs).0/24 | grep axis | cut -d"(" -f2 | cut -d ")" -f1

# Perhaps need: ^
# sudo apt install nmap net-tools

# For autostart, make sure xfce4-terminal is installed. Better for background images

sleep 10
#
oldport=$(lsof -i :5000 | cut -d" " -f2 | tail -n1)

if [ -z "$oldport" ]; then
    echo "No port in use..."
else
    kill $oldport && echo "Old stuff killed."
fi

cd ~/git/priv/maxlew_videosystem && python3 app.py &

sleep 3

google-chrome --app="http://localhost:5000/splashscreen" &

sleep 1

xdotool key F11
