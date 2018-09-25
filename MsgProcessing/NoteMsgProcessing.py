# coding=UTF-8

import itchat
import re

from StaticValues import temp_msgs_cache
from itchat.content import *


def deal_with_note(msg):
    # double check msg type
    if msg["Type"] != NOTE:
        return

    if u"撤回了一条消息" in msg["Content"]:
        deal_with_withdraw(msg)


def deal_with_withdraw(msg):
    msg_id = re.search("\<msgid\>(.*?)\</msgid\>", msg["Content"]).group(1)
    if msg_id in temp_msgs_cache:
        msg_content = u"[%s]撤回了消息[%s]" % (msg['ActualNickName'], temp_msgs_cache[msg_id])
        itchat.send(msg_content, toUserName=msg['FromUserName'])
