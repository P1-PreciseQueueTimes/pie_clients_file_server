import pyshark
import time
import os
import requests
import socket
import subprocess

url_file = open("url.txt","r")

base_url = url_file.read().strip() 

base_post_url = base_url + "/post/testing/receiver"

base_post_start = base_url + "/post/testing/receiver/start"

base_post_twr = base_url + "/post/testing/receiver/twr"

base_post_err = base_url + "/post/testing/err"

host_name = socket.gethostname()

wifi_interface = "wlan1"
sender_mac = "dc:a6:32:54:ac:ad"
channel = 13
user = ""

set_time = False

old_mac = ""
old_time = 0

capture = pyshark.LiveCapture(interface=wifi_interface)

out_obj = {
    "host_name": host_name
}

requests.post(base_post_start, json=out_obj)

t_rp = 0
t_sr = 0
t_rf = 0

scan_once = False


def print_info(packet):
    global old_mac, old_time,time_offset,t_rp,t_sr,t_rf, scan_once
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
                if not scan_once: 
                    t_rp = current_time

                    time.sleep(5)

                    subprocess.run(["wpa_cli","-i","wlan0","scan"])
                    t_sr = time.time_ns()
                    scan_once = True
                else:
                    t_rf = current_time

                    out_obj = {"host_name":host_name,"t_rp":t_rp,"t_sr":t_sr,"t_rf":t_rf}

                    requests.post(base_post_twr, json=out_obj)

                    scan_once = False

                print("received signal")
                signal_strength = packet["WLAN_RADIO"].signal_dbm

                out_obj = {
                    "host_name": host_name,
                    "internal_time": current_time ,
                    "signal_strength": signal_strength,
                }

                requests.post(base_post_url, json=out_obj)

                old_time = current_time

            old_mac = packet["WLAN"].ta
    except Exception as e:
        out_obj = {"host_name":host_name,"err":str(e)}
        requests.post(base_post_err,json=out_obj)
        print("ERR")


out_str = f'airmon-ng start "{wifi_interface}" {channel} >/dev/null 2>&1'
os.system("echo %s|sudo -S %s" % (user, out_str))

for packet in capture.sniff_continuously():
    print_info(packet)

