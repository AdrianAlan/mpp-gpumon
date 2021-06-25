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

if __name__ == '__main__':
    app.run()
