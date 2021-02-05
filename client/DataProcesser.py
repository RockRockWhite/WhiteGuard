"""02.05 16:04"""

import re


class DataProcesser:
    """"用于处理和解析数据"""

    def __init__(self):
        super().__init__()

    def connect(self, Addr):
        """
        POST WhiteGuard
        Addr: 192.168.1.1
        Type: connect
        """
        data = "POST WhiteGuard"
        data += "\nAddr: "
        data += str(Addr)
        data += "\nType: connect"
        data += "\n"
        return data

    def disconnect(self, Addr):
        """
        POST WhiteGuard
        Addr: 192.168.1.1
        Type: disconnect
        """
        data = "POST WhiteGuard"
        data += "\nAddr: "
        data += str(Addr)
        data += "\nType: disconnect"
        data += "\n"
        return data

    def ok(self, Addr):
        """
        WhiteGuard
        Addr: 192.168.1.1
        Type: ok
        """
        data = "WhiteGuard"
        data += "\nAddr: "
        data += str(Addr)
        data += "\nType: ok"
        data += "\n"
        return data

    def five_tumple(self, Addr, ip_src, ip_dst, proto, Sport, Dport, Len):
        """
        POST WhiteGuard
        Addr: 192.168.1.1
        Type: five_tumple
        Proto: TCP
        Ip_src: 58.251.81.111
        Sport: 443
        Ip_dst: 192.168.199.2
        Dport: 53
        Len: 128

        """
        data = "POST WhiteGuard"
        data += "\nAddr: "
        data += str(Addr)
        data += "\nType: five_tumple"
        data += "\nProto: "
        data += proto
        data += "\nIp_src: "
        data += ip_src
        data += "\nSport: "
        data += str(Sport)
        data += "\nIp_dst: "
        data += ip_dst
        data += "\nDport: "
        data += str(Dport)
        data += "\nLen: "
        data += str(Len)
        data += "\n"
        return data

    def process(self, data):
        """处理数据并返回字典"""
        data_header = re.findall("(.*?) WhiteGuard", data)
        data_name = re.findall("\n(.*?):", data)
        data_contain = re.findall(": (.*?)\n", data)
        data_dict = {}
        length = len(data_name)
        for cnt in range(length):
            data_dict[data_name[cnt]] = data_contain[cnt]
        if data_header == []:
            header = "RESPONE"
        else:
            header = data_header[0]
        return header, data_dict


'''
测试部分

data_processer = DataProcesser()
data = data_processer.connect("192.186.1.1")


str = """
WhiteGuard
Addr: 192.168.1.1
Type: ok
"""


data_header, data_dict = data_processer.process(str)
print("header = {}".format(data_header))
print("dict = {}".format(data_dict))
'''
