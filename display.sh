#!/bin/sh
# display.sh - Douban FM LCD display routines

trap 'exit 1' SIGINT

while true
do
    name=$(fmc -a localhost -p 10098 info | sed -n 2p | awk -F- '{print $1;}' | sed 's/^ *//; s/; */;/g')
    echo $name > /dev/ttyATH0
    
    title=$(fmc -a localhost -p 10098 info | sed -n 2p | awk -F- '{print $2;}' | sed 's/^ *//; s/; */;/g')
    echo $title > /dev/ttyATH0

    sleep 1
done

