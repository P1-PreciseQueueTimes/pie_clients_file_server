import requests
import time
import subprocess

base_url = "https://till-palmer-nt-areas.trycloudflare.com" 

post_url = base_url + "/post/testing/sender"

request_number = 0

while True:
    t = time.time_ns()
    subprocess.run(["wpa_cli" ,"-i" ,"wlan0", "scan"])
    request_number += 1

    out_obj = {"request_number":request_number,"internal_time":t}

    requests.post(post_url, json = out_obj)

    time.sleep(8)






