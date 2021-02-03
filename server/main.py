from Server import Server
from WebServer import WebServer
import threading
import time
import schedule

server = Server("", 2332)
web_server = WebServer()


def server_threading():
    """用于启动服务器进程的函数"""

    server.start()


def web_server_threading():
    """用于启动网站服务器进程的函数"""

    web_server.run("", 5000)


def update():
    """更新网页信息"""
    # 更新流量信息
    tumple_dict = server.get_tumple_dict()
    web_server.calculate_five_tumple(tumple_dict)
    print(tumple_dict)


def main():
    """主函数"""
    t_s = threading.Thread(target=server_threading)
    t_w = threading.Thread(target=web_server_threading)
    t_s.start()
    t_w.start()
    # 定时运行更新任务
    schedule.every(10).seconds.do(update)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
