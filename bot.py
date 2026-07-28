#!/usr/bin/env python

from deltabot_cli import BotCli
from deltachat2 import MessageData, events

cli = BotCli("gallerybot")

@cli.on(events.NewMessage)
def echo(bot, accid, event):
    msg = event.msg
    reply = MessageData(text=msg.text)
    bot.rpc.send_msg(accid, msg.chat_id, reply)

if __name__ == "__main__":
    cli.start()
