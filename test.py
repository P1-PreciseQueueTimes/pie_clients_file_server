from scapy.all import *

sender = "dc:a6:32:54:ac:ad"
ssid = ""
interface = "wlan0"
dest = "ff:ff:ff:ff:ff:ff"


def send_probe_req(senderaddr, destaddr, ssid, interface):
        radiotap = RadioTap()    
        dot11 = Dot11(type=0, subtype=0x04, addr1=destaddr, addr2=senderaddr, addr3=destaddr)
        dot11_probe_req = Dot11ProbeReq() / Dot11Elt(ID="SSID", info=ssid)
        
        rates_content = b'\x00'
        rates  = Dot11Elt(ID='Rates', info=rates_content)
        
        frame = radiotap / dot11 / dot11_probe_req / rates
        sendp(frame, iface=interface)

send_probe_req(sender, dest, ssid, interface)
