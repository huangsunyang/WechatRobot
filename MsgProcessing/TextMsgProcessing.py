# coding=UTF-8

from itchat.content import *
from StaticValues import temp_msgs_cache
import StaticValues
import itchat
import sys
import StringIO
import contextlib


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def deal_with_text(msg):
    # double check not text, should not be here
    if msg["Type"] != TEXT:
        return

    # record in cache for at_least two minutes, for showing withdrawn message
    temp_msgs_cache[msg["MsgId"]] = msg["Content"]

    if is_command(msg):
        deal_with_command(msg)


def deal_with_command(msg):
    command = msg["Content"]
    if command.startswith(u"$code"):
        code = command[6:]
        output = None

        with stdoutIO() as s:
            exec code

        print StaticValues.self_user_id

        if msg['FromUserName'] != StaticValues.self_user_id:
            itchat.send(s.getvalue().decode('utf8'), toUserName=msg['FromUserName'])
        else:
            itchat.send(s.getvalue().decode('utf8'), toUserName=msg['ToUserName'])


def is_command(msg):
    return msg["Content"].startswith(u"$")
