# mpp-gpumon

## @Planets

```
cd /opt
git clone https://github.com/AdrianAlan/mpp-gpumon.git
cd /opt/mpp-gpumon
chmod +x service.sh gpustatd.sh
echo <THE_MAGIC_GOES_HERE> > keys/magic.txt
cp mpp-gpumon.service /etc/systemd/system
systemctl start mpp-gpumon.service
systemctl enable mpp-gpumon.service
```

## @Server

```
chmod +x keygen.sh
keygen.sh
run.sh
```

Plus a deamon to push to gitlab: `gitlabd.sh`. To be run as cronjob.

## @Slack/Heroku

Add `slackSigningSecret` and `slackToken`. Run `git add`, `commit` and `push heroku master`. Fix API URL in Slack console.
