import requests
import time
import subprocess
import socketio
import socket

def makeScan():
        """Sends a probe out"""
        global request_number
        subprocess.run(["wpa_cli","-i","wlan0","scan"]) #makes/sends probe to be recived by receivers
        t = time.time_ns()

        out_obj = {"request_number":request_number,"internal_time":t} #output message contains "time" and "request number" for debugging. 

        requests.post(post_url, json = out_obj)

        request_number += 1

host_name = socket.gethostname()

url_file = open("url.txt","r") #url to server. url is changed often.

base_url = url_file.read().strip() 

post_url = base_url + "/post/testing/sender"

post_url_start = base_url + "/post/testing/sender/start"

out_obj = {
    "host_name": host_name
}

requests.post(post_url_start, json=out_obj) #sends it's name to server to show it is active.

automatic = False

request_number = 0

sio = socketio.Client() #starts a thread for intercepting server-commands

@sio.on("manual scan") #makes a manuel scan if it isn't auto.
def handle_manula_scan(data):
	if not automatic:
		makeScan()

@sio.on("automatic scan") #Turns automatic scanning on/off.
def handle_automatic_scan(data):
	global automatic
	automatic = not automatic

sio.connect(base_url) #connects to server

while True: #Makes and automatic scan every 8 seconds, if turned on.
    if automatic == True:
        makeScan()
        time.sleep(20)
