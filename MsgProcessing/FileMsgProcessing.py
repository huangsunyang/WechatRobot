from StaticValues import temp_msgs_cache
from MsgProcessing.PictureMsgProcessing import deal_with_picture
from itchat.content import *

import os
import re


def deal_with_file(msg):
    file_name = msg.fileName
    search_result = re.search('md5=\"(.*?)\"', msg['Content'])

    if search_result is not None:
        md5 = search_result.group(1) + '.' + file_name.split('.')[-1]
    else:
        md5 = file_name
    print file_name, md5

    if not os.path.exists(md5):
        msg.download(msg.fileName)
        os.rename(msg.fileName, md5)

    temp_msgs_cache[msg['MsgId']] = (ATTACHMENT, md5)