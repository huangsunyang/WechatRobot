#coding=UTF-8
import json
import pprint


class Debug:
    def __init__(self):
        pass

    @staticmethod
    def log_msg_neatly(msg):
        key_list = ["ActualNickName", "FromUserName", "ToUserName", "CreateTime", "MsgId", "Content"]
        for key in key_list:
            print key, msg[key]


if __name__ == '__main__':
    exec("print '中文'")