from scapy.all import *


class Sniffer:
    """用于抓取包的类"""

    def __init__(self):
        super().__init__()

    def sniff_once(self):
        dpkt = sniff(count=1)
        if str(dpkt[0][Ether].type) == "2048":
            ip_src = dpkt[0][IP].src
            ip_dst = dpkt[0][IP].dst
            proto = ""
            sport = 0
            dport = 0
            if str(dpkt[0][IP].proto) == "6":
                proto = "TCP"
                sport = dpkt[0][proto].sport
                dport = dpkt[0][proto].dport
            if str(dpkt[0][IP].proto) == "17":
                proto = "UDP"
                sport = dpkt[0][proto].sport
                dport = dpkt[0][proto].dport
            if str(dpkt[0][IP].proto) == "1":
                proto = "ICMP"
                sport = 0
                dport = 0

            return ip_src, ip_dst, proto, sport, dport
        else:
            return "", "", "", 0, 0
