# coding=UTF-8

from itchat.content import *
from StaticValues import temp_msgs_cache
from Utils.ThreadPool import thread_pool
from Utils.Timer import time_manager

import StaticValues
import itchat
import sys
import StringIO
import contextlib
import traceback



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
        thread_pool.add_task(python_code_func(code, msg), time_limit=5)


def exec_code(code):
    exec code


def python_code_func(code, msg):
    # the function on another thread
    def ret_func():
        with stdoutIO() as s:
            try:
                exec_code(code)
            except:
                print traceback.format_exc()

        content = s.getvalue().decode('utf8')

        if msg['FromUserName'] != StaticValues.self_user_id:
            itchat.send(content, toUserName=msg['FromUserName'])
        else:
            itchat.send(content, toUserName=msg['ToUserName'])

    return ret_func


def is_command(msg):
    return msg["Content"].startswith(u"$")
