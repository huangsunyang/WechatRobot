#coding=utf8

import itchat


def deal_with_picture(msg):
    print msg.fileName
    msg.download(msg.fileName)
    pass