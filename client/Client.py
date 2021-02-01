import socket
from DataProcesser import DataProcesser


class Client:
    def __init__(self, addr, port):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((addr, port))

    def send_data(self, data):
        # TODO
        self.server_socket.send(data.encode("utf-8"))

    def get_host_ip(self):
        ip = self.server_socket.getsockname()[0]
        return ip

    def close_socket(self):
        self.server_socket.close()

    def get_respone(self):
        respone = self.server_socket.recv(1024)
        return respone.decode("utf-8")


"""
这里是测试部分

# 初始化数据处理器
data_processer = DataProcesser()
# 创建客户端
client = Client("192.168.199.129", 2222)
# 发送连接数据
data_connect = data_processer.connect("")
client.send_data(data_connect)
# 等待OK返回
respone = client.get_respone()
# 处理返回数据
resopne_header, respone_dict = data_processer.process(respone)
if resopne_header == "RESPONE" and respone_dict["Type"] == "ok":
    print("连接服务器成功!")


while True:
    data = input("请输入数据:")
    if data == "close":
        data_close = data_processer.disconnect("")
        client.send_data(data_close)
        # 等待OK返回
        respone = client.get_respone()
        # 处理返回数据
        resopne_header, respone_dict = data_processer.process(respone)
        if resopne_header == "RESPONE" and respone_dict["Type"] == "ok":
            print("断开服务器连接.")
            break
    client.send_data(data)

client.close_socket()

"""