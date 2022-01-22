#  _____  _       _              _                 
# |  __ \| |     | |            (_)                
# | |__) | |_   _| |_ ___  _ __  _ _   _ _ __ ___  
# |  ___/| | | | | __/ _ \| '_ \| | | | | '_ ` _ \ 
# | |    | | |_| | || (_) | | | | | |_| | | | | | |
# |_|    |_|\__,_|\__\___/|_| |_|_|\__,_|_| |_| |_|
from asyncio import sleep
import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.errors import ChatSendMediaForbidden, SlowmodeWait, FloodWait, UsernameNotOccupied, \
    UserAlreadyParticipant, UsernameInvalid

# Join
one_time_sub_limit = 10
delay = 600
# Spam
spam_posts = ["1st"]

used_filters = filters.channel
last_media_group_id = None
app = Client("my_account", workers=1)


@app.on_message(used_filters)
async def spam(_, message):
    if (message.edit_date is None or (datetime.utcfromtimestamp(message.edit_date) - datetime.utcfromtimestamp(
            message.date)).total_seconds() > 5):
        # print("Raw message caught..") DEV
        return

    global last_media_group_id

    if (last_media_group_id == message.media_group_id) and message.media_group_id:
        # print("2+ photo message caught.. ", message.media_group_id) DEV
        return

    linked = await get_linked(message)
    await sleep(0.25)

    msg = await app.get_history(linked, limit=1)
    await sleep(0.25)

    for post in spam_posts:
        try:
            await app.send_message(msg[0].chat.id, post, reply_to_message_id=msg[0].message_id)
        except ChatSendMediaForbidden:
            await sleep(0.25)
            await app.send_message(msg[0].chat.id, post, reply_to_message_id=msg[0].message_id)
        except SlowmodeWait:
            continue
        await sleep(0.25)
    last_media_group_id = message.media_group_id
    print("Answered to: " + message.chat.title)


async def get_linked(msg):
    channel = await app.get_chat(msg.sender_chat.id)
    return channel.linked_chat.id


app.run()
