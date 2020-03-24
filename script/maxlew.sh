#!/usr/bin/env sh

# Needed software
#
# google chrome
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo apt install ./google-chrome-stable_current_amd64.deb
#
# xdotool
# sudo apt-get install xdotool
sleep 10
#
oldport=$(lsof -i :5000 | cut -d" " -f2 | tail -n1)

if [ -z "$oldport" ]; then
    echo "No port in use..."
else
    kill $oldport && echo "Old stuff killed."
fi

cd ~/git/priv/python-ip && python3 app.py &

sleep 3

google-chrome --app="http://localhost:5000/splashscreen" &

sleep 1

xdotool key F11
