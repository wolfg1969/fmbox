#!/bin/sh
# interface.sh - DoubanFM User Interface Script
# 2012-09-02 Guo Yong http://guoyong.me
# inspired by "Building a Wifi Radio" - http://mightyohm.com/blog/2008/10/building-a-wifi-radio-part-1-introduction/
#

# Some configuration settings
VOLUME=8
if [ ! -f /tmp/fm_channels ]; then
	echo "fm_channels file not found"
	exit 1
fi
#CHANNELS=$( tr ",{" "\n{" < /tmp/fm_channels|grep channel_id |awk -F : '{print $2;}'|tr '\n' ' ')
#CHANNELS_COUNT=$(echo $CHANNELS | awk '{n=split($0, array, " ")} END{print n }')
CHANNELS_COUNT=11
MAXADC=1024

#echo $CHANNELS
#echo $CHANNELS_COUNT


ADCBIN=$(expr "(" $MAXADC / $CHANNELS_COUNT ")" + 1)
#echo $ADCBIN

trap 'kill $! ; exit 1' SIGINT	# exit on ctrl-c, useful for debugging
				# kills the display.sh process before exiting

stty 9600 -echo < /dev/ttyATH0	# set serial port to 9600 baud
				# so we can talk to the AVR
				# turn off local echo to make TX/RX directions
				# completely separate from each other
# fmd setup
# fmd -a localhost -p 10098 chvol $VOLUME
volumecontrol Speaker $VOLUME

oldchannel=-1	# var to keep track of what station we're playing

echo "fmbox init^" > /dev/ttyATH0

# launch LCD display routines in the background
/root/display.sh &


while true	# loop forever
do
   inputline="" # clear input
  
   until inputline=$(echo $inputline | grep -e "^tuner: ")
   do
      inputline=$(head -n 1 < /dev/ttyATH0)
      #echo $inputline
   done
   value=$(echo $inputline | sed 's/tuner: //')	# strip out the tuner: part
   #echo $value
  
   # compute channel id based on tuner value
   # the tuner range is 0 to MAXADC
   channel_id=$(expr $value / $ADCBIN)
   #echo "channel=$channel_id"

   # if channel has changed, we need to tell fmd to change the channel
   if [ "$channel_id" -ne "$oldchannel" ]
   then
   	#echo "Tuner Position: " $value
   	#echo "New channel..." $channel_id
   	fmc -a localhost -p 10098 setch $channel_id
   fi
    
   oldchannel=$channel_id	# remember the new channel
done

