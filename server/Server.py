import socket
import threading
from FiveTumple import FiveTumple
from DataProcesser import DataProcesser


class Server:
    def __init__(self, addr, port):
        super().__init__()
        # 创建套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定接口
        self.server_socket.bind((addr, port))
        # 设置监听
        self.server_socket.listen(128)
        # 初始化数据处理器
        self.data_processer = DataProcesser()
        # 初始化用于保存五元组的字典
        self.five_tumple_dict = {}
        # 初始化保存五元组数量的字典
        self.five_tumple_cnt = 0

    def start(self):
        """接收客户端请求"""
        # 等待用户
        while True:
            client_socket, addr = self.server_socket.accept()
            self.t = threading.Thread(
                target=self.service_clinet, args=(client_socket, addr)
            )
            self.t.start()
            print("新的客户端 {} 连接成功!".format(addr[0]))
        self.server_socket.close()

    def service_clinet(self, client_socket, addr):
        """为客户端服务"""
        while True:
            # 接收数据
            request = client_socket.recv(1024)

            # 处理数据
            request_header, request_dict = self.data_processer.process(
                request.decode("utf-8")
            )

            # 对应的请求进行服务
            if request_header == "POST":
                if request_dict["Type"] == "connect":
                    """处理连接请求"""
                    self.connect(client_socket)

                if request_dict["Type"] == "disconnect":
                    """处理关闭请求"""
                    self.disconnect(client_socket)
                    break

                if request_dict["Type"] == "five_tumple":
                    """处理五元组"""
                    self.five_tumple(client_socket, request_dict)

                """ 用作测试 查看收到的内容,必要时候再打开
                if request:
                print(
                    "A new data from {0} data:\n\n{1}\n\n".format(
                        addr[0], request.decode("utf-8")
                    )
                )"""
        client_socket.close()
        print("客户端 {} 断开连接.`".format(addr[0]))

    def send_data(self, client_socket, data):
        client_socket.send(data.encode("utf-8"))

    def connect(self, client_socket):
        # 返回OK
        data_ok = self.data_processer.ok("")
        self.send_data(client_socket, data_ok)

    def disconnect(self, client_socket):
        # 返回OK
        data_ok = self.data_processer.ok("")
        self.send_data(client_socket, data_ok)

    def five_tumple(self, client_socket, request_dict):
        # 返回OK
        data_ok = self.data_processer.ok("")
        self.send_data(client_socket, data_ok)

        # 获得五元组和地址
        addr = request_dict["Addr"]
        five_tumple = FiveTumple(
            request_dict["Proto"],
            request_dict["Ip_src"],
            request_dict["Sport"],
            request_dict["Ip_dst"],
            request_dict["Dport"],
        )
        self.add_tumple(addr, five_tumple)
        print(
            "接收到客户端 {5} 发来的五元组 \t{2}\t{0}:{1}\t->\t{3}:{4}\t".format(
                five_tumple.Ip_src,
                five_tumple.Sport,
                five_tumple.Proto,
                five_tumple.Ip_dst,
                five_tumple.Dport,
                addr,
            )
        )
        self.five_tumple_cnt += 1

    def get_five_tumple_cnt(self):
        """获得五元组数量 并且重置"""
        cnt = self.five_tumple_cnt
        self.five_tumple_cnt = 0
        return cnt
    
    def get_tumple_dict(self):
        dict = self.five_tumple_dict
        self.five_tumple_dict.clear()
        return dict

    def add_tumple(self, addr, five_tumple):
        # 判断是否已存在该ip
        if self.five_tumple_dict.get(addr):
            # 存在则往其中在添加数据
            self.five_tumple_dict[addr].append(five_tumple)
        else:
            # 不存在则新建这个字典
            # 创建空list
            self.five_tumple_dict[addr] = []
            # 往这个list中添加元素
            self.five_tumple_dict[addr].append(five_tumple)

        # print(self.five_tumple_dict)


def main():
    """
    测试
    """
    server = Server("", 2332)
    server.start()


if __name__ == "__main__":
    main()
