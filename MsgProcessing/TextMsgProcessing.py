from itchat.content import *
import itchat


def deal_with_text(msg):
    if msg["Type"] != TEXT:
        return
