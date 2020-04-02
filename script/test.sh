#!/usr/bin/env bash

filepath="../ips.txt"

content=$(cat "$filepath")

for item in "${content[@]}"
do
    read -p "The name for ip: $item? " name
    
done
