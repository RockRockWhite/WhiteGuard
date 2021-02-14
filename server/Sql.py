"""
mysql> create table Tuples
    -> (
    -> Addr varchar(255),
    -> Proto varchar(255),
    -> Ip_src varchar(255),
    -> Sport varchar(255),
    -> Ip_dst varchar(255),
    -> Dport varchar(255),
    -> Len int,
    -> Time varchar(255)
    -> );
"""
from FiveTumple import FiveTumple
import pymysql


class Mysql:
    def __init__(self):
        """初始化数据库"""
        self.db = pymysql.connect(host="localhost",
                                  user="root",
                                  password="white",
                                  database="WhiteGuard"
                                  )

    def insert(self, addr, tuple, time):
        """用于将五元组信息提交到数据库"""
        commond = '''insert into Tuples values("{0}","{1}","{2}","{3}","{4}","{5}",{6},"{7}")''' \
            .format(addr, tuple.Proto, tuple.Ip_src,
                    tuple.Sport, tuple.Ip_dst, tuple.Dport,
                    tuple.Len, time)
        cursor = self.db.cursor()
        cursor.execute(commond)
        self.db.commit()