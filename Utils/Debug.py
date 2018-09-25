#coding=UTF-8
import json
import pprint


class Debug:
    def __init__(self):
        pass

    @staticmethod
    def log_msg_neatly(msg):
        key_list = ["ActualNickName", "FromUserName", "ToUserName", "CreateTime", "MsgId", "Content",
                    "Type", "Text", "MsgType", "SubMsgType"]

        longest_key_len = len(max(key_list, key=len))

        print "+------------------------------------+"
        for key in key_list:
            print key, Debug.spaces(longest_key_len - len(key)), msg[key]
        print "+------------------------------------+"

    @staticmethod
    def spaces(num):
        return ' ' * num


if __name__ == '__main__':
    exec("print '中文'")