# -*- coding=utf8 -*-
from itchat.content import *

import time

__author__ = 'huangsunyang'


class TextLengthRecorder(object):
    """
    发言字数统计,分小时记录,每个整点（非睡眠时间播报发言字数）
    """

    # {名字: {7点: 字数, 8点: 字数, 9点:字数, ...}
    text_length_dict = {}

    @staticmethod
    def record_msg_length(msg):
        TLR = TextLengthRecorder

        if msg['Type'] != TEXT:
            return

        actual_nickname = msg['ActualNickName']
        length = len(msg["Content"])
        hour = time.localtime().tm_hour

        TLR.record_text_with_time(actual_nickname, hour, length)

    @staticmethod
    def record_text_with_time(from_name, hour, text_length):
        """
        记录一个人在某个时间里发言多少字
        :param from_name:
        :param hour:
        :param text_length:
        :return:
        """
        TLR = TextLengthRecorder

        if from_name not in TLR.text_length_dict:
            TLR.text_length_dict[from_name] = dict()
        hour_length_dict = TLR.text_length_dict[from_name]

        if hour not in hour_length_dict:
            hour_length_dict[hour] = 0

        hour_length_dict[hour] += text_length

    @staticmethod
    def length_with_name_hour(name, hour):
        text_length_dict = TextLengthRecorder.text_length_dict

        if name not in text_length_dict:
            return 0
        if hour not in text_length_dict[name]:
            return 0
        return text_length_dict[name][hour]

    @staticmethod
    def cur_hour_ouput_statistics():
        text_length_dict = TextLengthRecorder.text_length_dict

        cur_hour = time.localtime().tm_hour
        output_msg = u'从{0}点到现在为止:\n'.format(cur_hour)
        for name in text_length_dict:
            output_msg += u"{0}发言{1}字\n".format(name,\
                                             TextLengthRecorder.length_with_name_hour(name, cur_hour))

        return output_msg

