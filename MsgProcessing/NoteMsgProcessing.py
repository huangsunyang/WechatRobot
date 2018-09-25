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
        msg_type, msg_content = temp_msgs_cache[msg_id]
        if msg_type == TEXT:
            to_send_msg_content = u"[%s]撤回了消息[%s]" % (msg['ActualNickName'], msg_content)
            itchat.send(to_send_msg_content, toUserName=msg['FromUserName'])
        elif msg_type == PICTURE:
            to_send_msg_content = u"[%s]撤回了以下图片" % msg['ActualNickName']
            itchat.send(to_send_msg_content, toUserName=msg['FromUserName'])
            pic_name = msg_content
            itchat.send_image(pic_name, toUserName=msg['FromUserName'])
        elif msg_type == VOICE:
            to_send_msg_content = u"[%s]撤回了以下音频" % msg['ActualNickName']
            itchat.send(to_send_msg_content, toUserName=msg['FromUserName'])
            mp3_name = msg_content
            itchat.send_file(mp3_name, toUserName=msg['FromUserName'])
        elif msg_type == ATTACHMENT:
            to_send_msg_content = u"[%s]撤回了以下文件" % msg['ActualNickName']
            itchat.send(to_send_msg_content, toUserName=msg['FromUserName'])
            file_name = msg_content
            itchat.send_file(file_name, toUserName=msg['FromUserName'])
