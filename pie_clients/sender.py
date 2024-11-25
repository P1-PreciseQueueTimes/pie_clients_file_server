import requests
import time
import subprocess

url = "https://washington-removed-explore-designer.trycloudflare.com/post/testing/sender"

request_number = 0

while True:
    t = time.time_ns()
    subprocess.run("wpa_cli -i wlan0 scan")
    request_number += 1

    out_obj = {"request_number":request_number,"internal_time":t}

    requests.post(url, json = out_obj)

    time.sleep(8)






