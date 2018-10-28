# -*- coding=utf8 -*-
from itchat.content import *
import matplotlib.pyplot as plt
import seaborn as sns
import os
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
        """
        获取某个人在[hour, cur_hour]之间的发言字数
        :param name:
        :param hour:
        :return:
        """
        text_length_dict = TextLengthRecorder.text_length_dict

        if name not in text_length_dict:
            return 0
        if hour not in text_length_dict[name]:
            return 0
        return text_length_dict[name][hour]

    @staticmethod
    def cur_hour_ouput_statistics():
        """
        获取记录的所有人在当前这个小时的发言字数
        :return:
        """
        text_length_dict = TextLengthRecorder.text_length_dict

        cur_hour = time.localtime().tm_hour
        output_msg = u'从{0}点到现在为止:\n'.format(cur_hour)
        for name in text_length_dict:
            output_msg += u"{0}发言{1}字\n".format(name,\
                                             TextLengthRecorder.length_with_name_hour(name, cur_hour))

        return output_msg

    @staticmethod
    def cur_hour_output_stat_image():
        text_length_dict = TextLengthRecorder.text_length_dict
        cur_hour = time.localtime().tm_hour
        name_list = text_length_dict.keys()
        length_list = [TextLengthRecorder.length_with_name_hour(name, cur_hour)
                       for name in name_list]
        x = u"你和我"
        y = u"{0}点到现在为止的发言字数".format(cur_hour)
        print name_list
        return TextLengthRecorder.barplot(name_list, length_list, x=x, y=y)

    @staticmethod
    def barplot(key, value, x=None, y=None):
        sns.set(style='darkgrid', palette='muted', color_codes=True, font='SimHei')
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

        barplot = sns.barplot(key, value)
        plt.xlabel(x)
        plt.ylabel(y)

        temp_stat_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        folder_name = 'temp'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_name = "{0}/{1}.png".format(folder_name, temp_stat_name)
        plt.savefig(file_name)
        return file_name

if __name__ == '__main__':
    TextLengthRecorder.barplot(["sdfa", 'asdf'], [1, 2])

