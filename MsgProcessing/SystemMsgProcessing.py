#coding=utf8

import itchat
import os
import re
from itchat.content import *
from Utils.Chat import reply_msg_from_chatroom
from StaticValues import temp_msgs_cache


def deal_with_system_event(msg):
    print msg
    if msg["MsgType"] == 51:
        deal_with_enter_chatroom_event(msg)


def deal_with_enter_chatroom_event(msg):
    content = u"%s悄悄地加入了群聊" % msg["ActualNickName"]
    # reply_msg_from_chatroom(msg, content)
    print content
