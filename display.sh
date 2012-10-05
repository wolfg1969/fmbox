#!/bin/sh
# display.sh - Douban FM LCD display routines

trap 'exit 1' SIGINT

stty 9600 -echo < /dev/ttyATH0
old_name=""
while true
do
    info=$(fmc -a localhost -p 10098 info | sed -n 2p)
    name=$(echo $info | awk -F- '{print $1;}' | sed 's/^ *//; s/; */;/g')
    if [ "$name" != "$old_name" ]; then
    	echo "fmbox clr" > /dev/ttyATH0
    	old_name=$name
    	title=$(echo $info | awk -F- '{print $2;}' | sed 's/^ *//; s/; */;/g')
    	echo "fmbox singer name^$name" > /dev/ttyATH0
    	echo "fmbox song name^$title" > /dev/ttyATH0
    	#echo "fmbox singer^$name" >> /tmp/display.log
    	#echo "fmbox song name^$title" >> /tmp/display.log
    fi

    sleep 1
done

