REPO=
JSON=$(curl -X GET http://127.0.0.1:5000/api/get/all)
cd $REPO
echo $JSON > status.json
git add status.json
git commit -m "Update" --author="Cron <cron@mpp-gpumon.cern>"
git push origin master
