from flask import Flask, redirect, render_template
from pyecharts.charts import Line
from Calculater import Calculater
from pyecharts import options as opts
from jinja2 import Markup

app = Flask(__name__)

in_cal = {}
out_cal = {}
# key为total的是统计所有主机的总包量
in_cal["total"] = [Calculater()] * 60
out_cal["total"] = [Calculater()] * 60


class WebServer:
    def __init__(self):
        super().__init__()

    def run(self, host, port, debug=False):
        app.run(host, port)

    def calculate_five_tumple(self, five_tumple):
        """"处理五元组的函数函数"""

        # 前移统计list
        self.pre_calculate()

        keys = list(five_tumple.keys())
        # 初始化dict
        for key in keys:

            if in_cal.get(key):
                in_cal[key][59].cnt = 0
            else:
                in_cal[key] = [Calculater()] * 60

            if out_cal.get(key):
                out_cal[key][59].cnt = 0
            else:
                out_cal[key] = [Calculater()] * 60

            # 遍历链表
            for cnt in range(len(five_tumple[key])):

                if five_tumple[key][cnt].Ip_dst == key:
                    # 这个包是入包
                    # 统计流量
                    in_cal["total"][59].cnt += 1
                    in_cal[key][59].cnt += 1
                    # 统计包长
                    in_cal["total"][59].len += int(five_tumple[key][cnt].Len)
                    in_cal[key][59].len += int(five_tumple[key][cnt].Len)
                else:
                    # 这个包是出包
                    # 统计流量
                    out_cal["total"][59].cnt += 1
                    out_cal[key][59].cnt += 1
                    # 统计包长
                    out_cal["total"][59].len += int(five_tumple[key][cnt].Len)
                    out_cal[key][59].len += int(five_tumple[key][cnt].Len)

    def pre_calculate(self):
        """用于将统计全部前移一格"""
        # 遍历dict
        in_keys = list(in_cal.keys())
        for in_key in in_keys:
            del in_cal[in_key][0]
            in_cal[in_key].append(Calculater())

        # 遍历dict
        out_keys = list(out_cal.keys())
        for out_key in out_keys:
            del out_cal[out_key][0]
            out_cal[out_key].append(Calculater())


@app.route("/")
def index():
    xaxis = []
    for i in range(60):
        xaxis.append(str(-i))

    # 统计入包流量和包长
    in_cnt = []
    in_len = []
    for calculater in in_cal["total"]:
        in_cnt.append(calculater.cnt)
        in_len.append(calculater.len)

    # 统计出包流量和包长
    out_cnt = []
    out_len = []
    for calculater in out_cal["total"]:
        out_cnt.append(calculater.cnt)
        out_len.append(calculater.len)

    line_cnt = Line().add_xaxis(xaxis[::-1]).add_yaxis("入包流量", in_cnt).add_yaxis("出包流量", out_cnt)

    line_len = Line().add_xaxis(xaxis[::-1]).add_yaxis("入包长度", in_len).add_yaxis("出包长度", out_len)
    return render_template("index.html", in_options=line_cnt.dump_options(), out_options=line_len.dump_options(),
                           in_dict=in_cal)


def main():
    """主函数"""
    print("")


if __name__ == "__main__":
    web_server = WebServer()
    web_server.run("", 5000, True)
