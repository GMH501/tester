import os
from subprocess import Popen
from signal import SIGTERM
from datetime import datetime

from psutil import Process
from flask import Flask, jsonify, render_template, url_for, session, redirect, request


def index():
    return render_template('index.html')


def start():
    if os.path.exists('/opt/bin/ffmpeg.pid'):
        with open('/opt/bin/ffmpeg.pid', 'r') as f:
            parentPid = f.read()
        parentProcess = Process(int(parentPid))
        return jsonify({'started': 'false', 'status': parentProcess.status()})
    parentProcess = Popen(startCmd(), shell=False)
    parentPid = parentProcess.pid
    with open('/opt/bin/ffmpeg.pid', 'w') as f:
        f.write(str(parentPid))
    parentProcess = Process(parentPid)
    return jsonify({'started': 'true', 'status': parentProcess.status()})


def stop():
    try:
        with open('/opt/bin/ffmpeg.pid', 'r') as pidFile:
            parentPid = pidFile.read()
    except:
            return jsonify({'stopped': 'false'})
    parentPid = int(parentPid)
    parentProcess = Process(parentPid)
    os.kill(parentPid, SIGTERM)
    os.system("rm -f /opt/bin/ffmpeg.pid")
    return jsonify({'stopped': 'true'})

def test():
    data = {"data": []}
    with os.scandir(r'C:\Users\gabriel.meghnagi\Documents\DEV\tester\tester\static\videos') as dir_contents:
        for entry in dir_contents:
            name = entry.name
            if 'mp4' in name:
                info = entry.stat()
                size = info.st_size
                mtime = info.st_mtime
                date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d-%H:%M')
                data["data"].append({"name" : name, "size": round(size / 1024 / 1024, 2), "date": date})
    return jsonify(data)


