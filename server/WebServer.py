from flask import Flask, redirect
from pyecharts.charts import Line
from pyecharts import options as opts
from jinja2 import Markup


app = Flask(__name__)

flow_list = [0] * 60


class WebServer:
    def __init__(self):
        super().__init__()

    def run(self, host, port, debug=False):
        app.run(host, port)

    def set_flow_list(self, flow):
        del flow_list[0]
        flow_list.append(flow)

    def get_flow_list(self):
        return flow_list


@app.route("/")
def hello():
    xaxis = []
    for i in range(60):
        xaxis.append(str(-i))
    line = Line().add_xaxis(xaxis[::-1]).add_yaxis("主机1", flow_list)
    return str(Markup(line.render_embed()))


def main():
    """主函数"""
    print("")


if __name__ == "__main__":
    web_server = WebServer()
    web_server.run("", 5000, True)
