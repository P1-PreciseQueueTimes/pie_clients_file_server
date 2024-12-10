"""Module for the code the receivers will run/execute."""
import pyshark
import time
import os
import requests
import socket

url_file = open("url.txt","r") #url to server. url is changed often.

base_url = url_file.read().strip() 

base_post_url = base_url + "/post/testing/receiver"

base_post_start = base_url + "/post/testing/receiver/start"

host_name = socket.gethostname()

wifi_interface = "wlan1"
sender_mac = "dc:a6:32:54:ac:ad" #specific mac-adresse to search for. Easier to scan for a specific device.
channel = 11 
user = ""

set_time = False

old_mac = ""
old_time = 0

mac_table={}

capture = pyshark.LiveCapture(interface=wifi_interface) #setup pyshark

out_obj = {
    "host_name": host_name
}

requests.post(base_post_start, json=out_obj) #sends it's name to server to show it is active.

def print_info(packet):
    global old_mac, old_time,time_offset, mac_table
    current_time = time.time_ns() 
    try:
        if not packet["WLAN.MGT"] or not packet["WLAN"] or not packet["WLAN_RADIO"]: #filters out wrong packages.
            return
        if not packet["WLAN"].ta: #checks if packet have a mac-adress.
            return

        if packet["WLAN"].fc_type_subtype == "0x0004":
            """
            if old_mac == packet["WLAN"].ta or (current_time - old_time) / 1000000.0 < 5000.0:
                return
            """

            if (packet["WLAN"].ta in mac_table):
                if (current_time-mac_table[packet["WLAN"].ta])/ 1000000.0 < 5000.0:
                    return
            mac_table[packet["WLAN"].ta]=current_time

            """if (current_time - old_time) / 1000000.0 < 5000.0:
                return
            if packet["WLAN"].ta == sender_mac: #checks mac-adress is the correct one."""
            
            print("received signal")
            signal_strength = packet["WLAN_RADIO"].signal_dbm

            out_obj = {
                "host_name": host_name,
                "internal_time": current_time ,
                "signal_strength": signal_strength,
                "mac_adress": packet["WLAN"].ta,
            }

            requests.post(base_post_url, json=out_obj) #sends data to server.

            old_mac = packet["WLAN"].ta
    except Exception:
        pass


out_str = f'airmon-ng start "{wifi_interface}" {channel} >/dev/null 2>&1' #linux command to setup antenna-sniffer
os.system("echo %s|sudo -S %s" % (user, out_str)) #writes/executes command into terminal

for packet in capture.sniff_continuously(): #Everytime it catches a packet, it writes/procceses it. it doesen't stop.
    print_info(packet)