import requests
import time
import subprocess
import socketio
import socket

url_file = open("url.txt","r")

def makeScan():
        global request_number
        subprocess.run(["wpa_clie","-i","wlan0","scan"])
        t = time.time_ns()

        out_obj = {"request_number":request_number,"internal_time":t}

        requests.post(post_url, json = out_obj)

        request_number += 1

host_name = socket.gethostname()

base_url = url_file.read().strip() 

post_url = base_url + "/post/testing/sender"

post_url_start = base_url + "/post/testing/sender/start"

out_obj = {
    "host_name": host_name
}

requests.post(post_url_start, json=out_obj)

automatic = False

request_number = 0

sio = socketio.Client()

@sio.on("manual scan")
def handle_manula_scan(data):
	if not automatic:
		makeScan()

@sio.on("automatic scan")
def handle_automatic_scan(data):
	global automatic
	automatic = not automatic
	print("auto")

sio.connect(base_url)

while True:
    if automatic == True:
        makeScan()
        time.sleep(8)
