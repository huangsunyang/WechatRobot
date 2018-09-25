import itchat
import StaticValues


def reply_msg_from_chatroom(msg, content):
    if msg['FromUserName'] != StaticValues.self_user_id:
        itchat.send(content, toUserName=msg['FromUserName'])
    else:
        itchat.send(content, toUserName=msg['ToUserName'])