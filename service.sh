#!/bin/sh

TIMER=300
URL=http://adrianalan:5000/api/set
HOSTDIR=$(dirname "$0")

while true
do
  sh $HOSTDIR/gpustatd.sh $URL
  sleep $TIMER
done
