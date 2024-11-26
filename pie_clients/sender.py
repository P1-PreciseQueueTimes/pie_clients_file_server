import requests
import time
import subprocess
import socketio

url_file = open("url.txt","r")

base_url = url_file.read().strip() 

post_url = base_url + "/post/testing/sender"

request_number = 0

sio =socketio.SimpleClient()

sio.connect(base_url)

while True:
    subprocess.run(["wpa_cli" ,"-i" ,"wlan0", "scan"])
    t = time.time_ns()
    request_number += 1

    out_obj = {"request_number":request_number,"internal_time":t}

    requests.post(post_url, json = out_obj)

    time.sleep(8)






