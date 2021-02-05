class FiveTumple:
    """用于保存五元组的类"""

    def __init__(self, Proto, Ip_src, Sport, Ip_dst, Dport, Len):
        super().__init__()
        self.Proto = Proto
        self.Ip_src = Ip_src
        self.Sport = Sport
        self.Ip_dst = Ip_dst
        self.Dport = Dport
        self.Len = Len
