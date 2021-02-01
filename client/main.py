import threading
from Sniff import Sniffer
from Client import *



closed = False

def handle_input(client, data_processer):
    while True:
        data = input("请输入数据:")
        if data == "close":
            # 设置关闭状态
            global closed
            closed = True
            break
        client.send_data(data)


def main():
    # 输出提示
    print("流量监控程序启动 监控中...")
    # 初始化数据处理器
    data_processer = DataProcesser()
    # 创建客户端
    client = Client("192.168.3.10", 2332)
    # 发送连接数据
    addr = client.get_host_ip()
    data_connect = data_processer.connect(addr)
    client.send_data(data_connect)
    # 等待OK返回
    respone = client.get_respone()
    # 处理返回数据
    resopne_header, respone_dict = data_processer.process(respone)
    if resopne_header == "RESPONE" and respone_dict["Type"] == "ok":
        print("连接服务器成功!")
    # 创建输入进程
    t = threading.Thread(target=handle_input, args=(client, data_processer))
    t.start()

    while True:
        """"抓包并且发送给服务器"""
        # 判断服务是否已经被关闭
        global closed
        if closed:
            # 关闭客户端
            data_close = data_processer.disconnect(addr)
            client.send_data(data_close)
            # 等待OK返回
            respone = client.get_respone()
            # 处理返回数据
            resopne_header, respone_dict = data_processer.process(respone)
            if resopne_header == "RESPONE" and respone_dict["Type"] == "ok":
                print("断开服务器连接.")
                client.close_socket()
                break
        # 抓包
        sniffer = Sniffer()
        ip_src, ip_dst, proto, sport, dport = sniffer.sniff_once()

        # 过滤ICMP协议和非IP协内容
        if proto == "ICMP" or proto == "":
            continue
        print(
            "五元组 {2} {0}:{3}\t->\t{1}:{4}\t".format(ip_src, ip_dst, proto, sport, dport)
        )
        five_temple_data = data_processer.five_tumple(
            addr, ip_src, ip_dst, proto, sport, dport
        )
        client.send_data(five_temple_data)
        # 等待OK返回
        respone = client.get_respone()
        # 处理返回数据
        resopne_header, respone_dict = data_processer.process(respone)
        if resopne_header == "RESPONE" and respone_dict["Type"] == "ok":
            print("发送成功.")


if __name__ == "__main__":
    main()
