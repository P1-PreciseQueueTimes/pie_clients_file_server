import requests
import time
import subprocess
import socketio
import socket
import pyshark
import os

url_file = open("url.txt","r")

wifi_interface = "wlan1"

receiver_mac = "dc:a6:32:54:ab:34"

channel = 13
user = ""

capture = pyshark.LiveCapture(interface=wifi_interface)

out_str = f'airmon-ng start "{wifi_interface}" {channel} >/dev/null 2>&1'
os.system("echo %s|sudo -S %s" % (user, out_str))


host_name = socket.gethostname()

base_url = url_file.read().strip() 

post_url = base_url + "/post/testing/sender"

post_url_start = base_url + "/post/testing/sender/start"

post_twr = base_url + "/post/testing/sender/twr"

base_post_err = base_url + "/post/testing/err"

def makeScan():
        global request_number,post_url,post_twr
        try:
            subprocess.run(["wpa_cli","-i","wlan0","scan"])
            t_sp = time.time_ns()
            t_rr = 0

            out_obj = {"request_number":request_number,"internal_time":t_sp}

            requests.post(post_url, json = out_obj)

            request_number += 1
            for packet in capture.sniff_continuously():
                current_time = time.time_ns()

                if not packet["WLAN.MGT"] or not packet["WLAN"] or not packet["WLAN_RADIO"]:
                    return
                if not packet["WLAN"].ta:
                    return
                if packet["WLAN"].fc_type_subtype == "0x0004":

                    if packet["WLAN"].ta == receiver_mac:
                        t_rr = current_time 
                        break
            time.sleep(8)

            subprocess.run(["wpa_cli","-i","wlan0","scan"])
            t_sf = time.time_ns()

            out_obj = {"host_name":host_name,"t_sp":t_sp,"t_rr":t_rr,"t_sf":t_sf}

            requests.post(post_twr, json = out_obj)
        except Exception as e:
            out_obj = {"host_name":host_name,"err":str(e)}
            requests.post(base_post_err,json=out_obj)
            print("ERR")

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
