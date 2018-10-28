import itchat
import StaticValues


class Chat(object):
    @staticmethod
    def get_from_user_in_msg(msg):
        if msg['FromUserName'] != StaticValues.self_user_id:
            return msg['FromUserName']
        else:
            return msg['ToUserName']

    @staticmethod
    def reply_text_from_chatroom(msg, content):
        toUserName = Chat.get_from_user_in_msg(msg)
        itchat.send(content, toUserName=toUserName)

    @staticmethod
    def reply_img_from_chatroom(msg, image_name):
        toUserName = Chat.get_from_user_in_msg(msg)
        itchat.send_image(image_name, toUserName=toUserName)
