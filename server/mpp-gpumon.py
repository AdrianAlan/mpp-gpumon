import json
import requests
import subprocess
import time
import yaml

from flask import Flask, jsonify, redirect, url_for, render_template, request
from database import GPUDatabase

app = Flask(__name__, template_folder="templates")
config = yaml.safe_load(open('server/mpp-gpumon.yml'))
db = GPUDatabase(url=config['database']['url'])


def set_state(planet, gid, timestamp, users):
    return db.set_state(planet, gid, users, timestamp)


def verify(key, magic, vcode, timestamp):
    t = time.time()
    # Filter requests older than 10s
    if (t - int(timestamp) > 10):
        return False
    # Decode the message
    c = ('echo -n "{}" | base64 -d |'
         'openssl rsautl -decrypt -inkey {} -in -').format(vcode, key)
    out = subprocess.check_output(c, shell=True)
    with open(magic) as f:
        s = f.read()
    # Verify authenticity
    return out.decode().rstrip() == str(timestamp) + s


@app.route('/api/set', methods=['POST'])
def set_api():
    content = request.get_json()
    planet = content['planet']
    gid = content['gid']
    users = content['usr']
    timestamp = content['t']
    vcode = content['v']
    key = config['key']
    magic = config['magic']
    if verify(key, vcode, timestamp):
        try:
            set_state(planet, gid, timestamp, users)
            r = jsonify(success=True)
        except Exception as e:
            r = jsonify(success=False)
    else:
        r = jsonify(success=False)
    return r


if __name__ == '__main__':
    app.run()
