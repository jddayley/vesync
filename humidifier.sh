#!/bin/bash
x=1
s=1
python3 mqserver.py > out.log &
 while [ $s -le 5 ]
 do
   echo "# of Humidifier $x samples"
   x=$(( $x + 1 ))
   python3 mqclient.py
   sleep 300
done
#python3 mqserver.py