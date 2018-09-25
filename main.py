# coding=UTF-8
import itchat
import re
import time

from itchat.content import *
from MsgProcessing import TextMsgProcessing

all_text_messages = {}


@itchat.msg_register(INCOME_MSG, isGroupChat=True)
def text_reply(msg):
    print msg["Content"]
    if msg['Type'] == 'Text':
        reply_content = msg['Text']
        all_text_messages[msg['MsgId']] = msg["Text"]
    elif msg['Type'] == 'Picture':
        reply_content = u"图片: " + msg['FileName']
    elif msg['Type'] == 'Card':
        reply_content = u" " + msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            reply_content = u"位置: 纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            reply_content = u"位置: " + location
    elif msg['Type'] == 'Note':
        if u'撤回了一条消息' in msg['Content']:
            msg_id = re.search("\<msgid\>(.*?)\</msgid\>", msg["Content"]).group(1)
            print msg_id
            if msg_id in all_text_messages:
                itchat.send(u"%s撤回了消息【%s】" % (msg['ActualNickName'], all_text_messages[msg_id]), toUserName=msg['FromUserName'])
            print msg["Content"]
        reply_content = u"通知"
    elif msg['Type'] == 'Sharing':
        reply_content = u"分享"
    elif msg['Type'] == 'Recording':
        reply_content = u"语音"
    elif msg['Type'] == 'Attachment':
        reply_content = u"文件: " + msg['FileName']
    elif msg['Type'] == 'Video':
        reply_content = u"视频: " + msg['FileName']
    else:
        reply_content = u"消息"

    print msg["FromUserName"]

    friend = itchat.search_chatrooms(userName=msg['FromUserName'])

    if friend is None:
        return

    itchat.send(u"Friend:%s -- %s\n"
                u"Time:%s\n"
                u" Message:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), reply_content),
                toUserName='filehelper')
    #itchat.send(u"我已经收到你在【%s】发送的消息【%s】稍后回复。--微信助手(Python版)" % (time.ctime(), reply_content),
             #   toUserName=msg['FromUserName'])


if __name__ == '__main__':
    itchat.auto_login()
    itchat.run()