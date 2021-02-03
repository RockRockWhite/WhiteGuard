from flask import Flask, redirect, render_template
from pyecharts.charts import Line
from pyecharts import options as opts
from jinja2 import Markup

app = Flask(__name__)

in_cnt = {}
out_cnt = {}
# key为total的是统计所有主机的总包量
in_cnt["total"] = [0] * 60
out_cnt["total"] = [0] * 60


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
        for key in keys:

            if in_cnt.get(key):
                in_cnt[key][59] = 0
            else:
                in_cnt[key] = [0] * 60

            if out_cnt.get(key):
                out_cnt[key][59] = 0
            else:
                out_cnt[key] = [0] * 60

            # 遍历链表
            for cnt in range(len(five_tumple[key])):

                if five_tumple[key][cnt].Ip_dst == key:
                    # 这个包是入包
                    in_cnt["total"][59] += 1
                    in_cnt[key][59] += 1
                else:
                    # 这个包是出包
                    out_cnt["total"][59] += 1
                    out_cnt[key][59] += 1

    def pre_calculate(self):
        """用于将统计全部前移一格"""
        # 遍历dict
        in_keys = list(in_cnt.keys())
        for in_key in in_keys:
            del in_cnt[in_key][0]
            in_cnt[in_key].append(0)

        # 遍历dict
        out_keys = list(out_cnt.keys())
        for out_key in out_keys:
            del out_cnt[out_key][0]
            out_cnt[out_key].append(0)


@app.route("/")
def index():
    xaxis = []
    for i in range(60):
        xaxis.append(str(-i))

    line_in = Line().add_xaxis(xaxis[::-1]).add_yaxis("入包流量", in_cnt["total"]).add_yaxis("出包流量", out_cnt["total"])

    line_out = Line().add_xaxis(xaxis[::-1]).add_yaxis("主机1", out_cnt["total"])
    return render_template("index.html", in_options=line_in.dump_options(), out_options=line_out.dump_options())


@app.route("/flash")
def flash():
    while True:
        xaxis = []
        for i in range(60):
            xaxis.append(str(-i))

        line_in = Line().add_xaxis(xaxis[::-1]).add_yaxis("入包流量", in_cnt["total"]).add_yaxis("出包流量", out_cnt["total"])

        line_out = Line().add_xaxis(xaxis[::-1]).add_yaxis("主机1", out_cnt["total"])
        return render_template("index.html", in_options=line_in.dump_options(), out_options=line_out.dump_options())


def main():
    """主函数"""
    print("")


if __name__ == "__main__":
    web_server = WebServer()
    web_server.run("", 5000, True)
