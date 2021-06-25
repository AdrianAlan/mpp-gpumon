mkdir -p keys
date +%s | sha256sum | base64 | head -c 32 > keys/magic.txt
chmod 600 keys/magic.txt
openssl genrsa -out keys/mppgpumon-prv.pem 1024
openssl rsa -in keys/mppgpumon-prv.pem -out keys/mppgpumon-pub.pem -outform PEM -pubout
