# coding=UTF-8
import itchat
import re
import time

from itchat.content import *
from MsgProcessing import TextMsgProcessing
from MsgProcessing import NoteMsgProcessing
from StaticValues import caring_friends_list
import StaticValues
from Utils.Debug import Debug


@itchat.msg_register(INCOME_MSG, isGroupChat=True)
def text_reply(msg):
    Debug.log_msg_neatly(msg)

    # only deal with message from certain friends
    if msg['ActualNickName'] not in caring_friends_list:
        return

    if msg['Type'] == TEXT:
        TextMsgProcessing.deal_with_text(msg)
        reply_content = msg["Content"]
    elif msg['Type'] == 'Note':
        NoteMsgProcessing.deal_with_note(msg)
        reply_content = u"通知"
    else:
        return

    friend = itchat.search_chatrooms(userName=msg['FromUserName'])

    if friend is None:
        return

    itchat.send(u"Friend:%s -- %s\n"
                u"Time:%s\n"
                u" Message:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), reply_content),
                toUserName='filehelper')


if __name__ == '__main__':
    itchat.auto_login()

    StaticValues.self_user_id = itchat.search_friends(name=u"黄孙扬")[0]["UserName"]

    itchat.run()