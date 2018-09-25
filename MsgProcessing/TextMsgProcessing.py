# coding=UTF-8

from itchat.content import *
from StaticValues import temp_msgs_cache
from Utils.ThreadPool import thread_pool
from Utils.Timer import time_manager
from sys import argv, executable
from tempfile import NamedTemporaryFile
from subprocess import check_output

import StaticValues
import itchat
import sys
import StringIO
import contextlib
import traceback
import Utils.Chat as Chat



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
    temp_msgs_cache[msg["MsgId"]] = (TEXT, msg["Content"])

    if is_command(msg):
        deal_with_command(msg)


def deal_with_command(msg):
    command = msg["Content"]
    if command.startswith(u"$code"):
        code = command[6:]
        thread_pool.add_task(python_code_func(msg, code), time_limit=5)


def exec_code(code):
    exec code


def python_code_func(msg, code):
    # the function on another thread
    def ret_func():
        with stdoutIO() as s:
            try:
                exec_code(code)
            except:
                print traceback.format_exc()

        content = s.getvalue().decode('utf8')
        Chat.reply_msg_from_chatroom(msg, content)


    return ret_func


def is_command(msg):
    return msg["Content"].startswith(u"$")
