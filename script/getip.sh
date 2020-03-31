#!/usr/bin/env sh

path="../ips.txt"

type nmap >/dev/null 2>&1 || { echo >&2 "I require nmap but it's not installed.  Aborting."; exit 1; }
type /sbin/ifconfig >/dev/null 2>&1 || { echo >&2 "I require ifconfig but it's not installed. Install it by running 'apt install net-tools'.  Aborting."; exit 1; }

nmap -sP $(/sbin/ifconfig | grep eno1 -a1 | tail -1 | sed -En 's/inet.([0-9]{3}.*)\s\snetmask.*/\1/p' | cut -d"." -f1-3 | xargs).0/24 | grep axis | cut -d"(" -f2 | cut -d ")" -f1 > "$path" || { echo >&2 "Something went wrong with the super command..."; exit 1; }

if [ -s "$path" ]
then
    echo "The file $path is created and contains the ipadresses."
    read -p "Do you want to doublecheck? [y/N] " answer
    if [ "$answer" = "y" ]; then
        cat "$path"
    fi
else
   echo "Something went wrong with the super command!!"
fi
