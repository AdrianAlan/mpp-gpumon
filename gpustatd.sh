HOSTDIR=

IFS='.' read -ra HOST <<< $(cat /etc/hostname)
TIMESTAMP=$(date +%s)
VERIFICATION=$(echo "$TIMESTAMP$(<$HOSTDIR/keys/magic.txt)" | /bin/openssl rsautl -encrypt -inkey $HOSTDIR/keys/mppgpumon-pub.pem -pubin | base64 -w 0)
GPUS=($(nvidia-smi -L | awk '{print substr($2, 1, length($2)-1)}'))

for i in "${GPUS[@]}"; do
  PID=($(nvidia-smi -i $i | grep python | awk '{print $5'}))
  NAME=()
  for j in "${!PID[@]}"; do
    USR=($(ps -up ${PID[j]} | awk 'NR>1{print $1}'))
    NAME+=($USR)
  done
  STR='{"planet":"'${HOST[0]}'","gid":"'${GPUS[i]}'","usr":"'$(IFS=","; shift; echo "$NAME")'","t":"'${TIMESTAMP}'","v":"'$VERIFICATION'"}'
  curl -X POST -H "Content-Type: application/json" -d $STR $1
done
