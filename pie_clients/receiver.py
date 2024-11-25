import pyshark
import time
import os
import requests
import socket
import subprocess

set_time = False

url = "https://louisiana-trading-courtesy-chris.trycloudflare.com/post/testing/receiver"

url_start = "https://louisiana-trading-courtesy-chris.trycloudflare.com/post/testing/receiver_start"

host_name = socket.gethostname() 

while not set_time:
	try:

		sync_time = requests.get("http://localhost:5000/get/testing/time").text

		subprocess.run(["sudo","date","+%s","-s",f"@{sync_time}"])
		set_time = True


	except Exception:
		pass

	out_obj = {"host_name":host_name,"connected":set_time}

	requests.post(url_start,json=out_obj)

wifi_interface = "wlan1" 
sender_mac = "58:cf:79:db:00:34"
channel = 13
user = ""


old_mac = ""
old_time = 0



capture = pyshark.LiveCapture(interface=wifi_interface)


def print_info(packet):
    global old_mac, old_time
    current_time = time.time_ns()
    try:
        if not packet["WLAN.MGT"] or not packet["WLAN"] or not packet["WLAN_RADIO"]:
            return
        if not packet["WLAN"].ta:
            return
        
        if packet["WLAN"].fc_type_subtype == "0x0004":
            if old_mac == packet["WLAN"].ta or (current_time - old_time) / 1000000.0 < 5000.0:
                return

            if packet["WLAN"].ta == sender_mac: 
                

                out_obj = {"host_name":host_name,"internal_time":current_time}

                requests.post(url,json=out_obj)

                old_time = current_time

            old_mac = packet["WLAN"].ta
    except Exception :
        pass

out_str = f'airmon-ng start "{wifi_interface}" {channel} >/dev/null 2>&1'
os.system("echo %s|sudo -S %s" % (user, out_str))

capture.apply_on_packets(print_info, packet_count=10000)#, timeout=50)
