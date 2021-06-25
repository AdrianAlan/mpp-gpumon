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


def get_user_full_name(user):
    c = "phonebook --homedir */{} | awk '{}'".format(user, '{print $2" "$1}')
    out = subprocess.check_output(c, shell=True)
    return out.decode()[:-1]


def get_state(planet):
    return db.get_state(planet)


def set_state(planet, gid, timestamp, users):
    return db.set_state(planet, gid, users, timestamp)


def pprint_users(users):
    return ', '.join([get_user_full_name(user) for user in users.split(',')])


def pprint_time(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(t)))


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


@app.route('/mpp-gpumon')
def index():
    stats = get_api('all', False)
    return render_template('mpp-gpumon.html', stats=stats)


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


@app.route('/api/get/<planets>')
def get_api(planets, json=True):
    response = []

    if planets == 'all':
        planets = config['planets']
    else:
        planets = planets.split(',')

    for planet in planets:
        item = {}
        r, state = [], get_state(planet)
        if state:
            for gpu in state:
                users = pprint_users(gpu['users'])
                gpu['time'] = pprint_time(gpu['time'])
                gpu['users'] = users
                r.append(gpu)
        item["name"] = planet
        item["details"] = r
        response.append(item)
    if json:
        return jsonify(response)
    else:
        return response


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
