#!/bin/sh

TIMER=300
URL=http://adrianalan:5000/api/set

while true
do
  sh gpustatd.sh $URL
  sleep $TIMER
done
