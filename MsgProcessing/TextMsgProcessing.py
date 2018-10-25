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
import re
import time
import sys
import StringIO
import contextlib
import traceback
import Utils.Chat as Chat
from Utils.Debug import Debug
from TextLengthRecorder import TextLengthRecorder
import functools


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


commands_dict = {}


# a wrapper to add a condition to commands_dict
def command_condition(func):
    if func not in commands_dict:
        commands_dict[func] = None
    else:
        Debug.log_warning("you are overwriting an existed command condition")
    return func


# a wrapper to add a function to a paired condition
def run_at_condition(condition):
    def wrapper(func):
        if condition not in commands_dict:
            Debug.log_error("condition not existed yet, please add condition first")
        else:
            if commands_dict[condition] is not None:
                Debug.log_warning("You are overwriting an existed command function")
            commands_dict[condition] = func
        return func
    return wrapper


def deal_with_text(msg):
    # double check not text, should not be here
    if msg["Type"] != TEXT:
        return

    # record text in cache to resend when someone withdraw the message
    record_withdraw_cache(msg)

    if not is_command(msg):
        # to record the length of a text
        TextLengthRecorder.record_msg_length(msg)

    # if the text is command, then do sth.
    deal_with_command(msg)


# record in cache for disable withdraw function
def record_withdraw_cache(msg):
    # record in cache for at_least two minutes, for showing withdrawn message
    temp_msgs_cache[msg["MsgId"]] = (TEXT, msg["Content"])


# to determine if a message is a command
def is_command(msg):
    for condition in commands_dict:
        if condition(msg):
            return True
    return False


def deal_with_command(msg):
    for condition, func in commands_dict.iteritems():
        if condition(msg):
            func(msg)


@command_condition
def is_code(msg):
    return msg["Content"].startswith(u"$code ")


@run_at_condition(is_code)
def deal_with_code(msg):
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


@command_condition
def is_remind(msg):
    return msg["Content"].startswith(u"$提醒")


@run_at_condition(is_remind)
def deal_with_remind(msg):
    remind_content = msg["Content"][3:].split(u' ')[0]

    print remind_content

    remind_time_since_now = 0

    for i in [u"小时", u"分", u"秒"]:
        remind_time_found = re.search(u"([0-9]*)" + i, msg["Content"])
        if remind_time_found is None:
            remind_time_since_now += 0
        else:
            remind_time_since_now += int(remind_time_found.group(1))
            remind_time_since_now *= 60

    remind_time_since_now /= 60
    print remind_time_since_now

    def remind_func():
        t = remind_time_since_now
        while t > 0:
            Chat.reply_msg_from_chatroom(msg, str(t))
            time.sleep(1)
            t -= 1
        Chat.reply_msg_from_chatroom(msg, remind_content)

    thread_pool.add_task(remind_func)


@command_condition
def is_length_stat(msg):
    return msg["Content"].startswith(u"$stat")


@run_at_condition(is_length_stat)
def deal_with_msg_length_stat(msg):
    stat = TextLengthRecorder.cur_hour_ouput_statistics()
    Chat.reply_msg_from_chatroom(msg, stat)
