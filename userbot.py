#  _____  _       _              _                 
# |  __ \| |     | |            (_)                
# | |__) | |_   _| |_ ___  _ __  _ _   _ _ __ ___  
# |  ___/| | | | | __/ _ \| '_ \| | | | | '_ ` _ \ 
# | |    | | |_| | || (_) | | | | | |_| | | | | | |
# |_|    |_|\__,_|\__\___/|_| |_|_|\__,_|_| |_| |_|


from asyncio import sleep
from datetime import datetime
from pyrogram import Client, filters

app = Client("my_account")
spam_text = '1st'
used_filters = filters.channel
send_as_chat = None


@app.on_message(used_filters)
async def spam(_, message):
    if (message.edit_date is None or (datetime.utcfromtimestamp(message.edit_date) - datetime.utcfromtimestamp(
            message.date)).total_seconds() > 5):
        return

    linked = await get_linked(message)
    await sleep(0.25)

    global send_as_chat
    if not send_as_chat:
        chats = await app.get_send_as_chats(linked)
        print("Available chats:")
        for index, chat in enumerate(chats, start=1):
            print(str(index) + ": " + chat.title)
        answer = int(input("Write ID of chat and press Enter: "))
        send_as_chat = chats[answer-1].id
    await app.set_send_as_chat(linked, send_as_chat)

    msg = await app.get_history(linked, limit=1)
    await sleep(0.25)

    await msg[0].reply_text(spam_text)
    await sleep(0.25)
    print("Answered to: " + message.chat.title)


async def get_linked(msg):
    channel = await app.get_chat(msg.sender_chat.id)
    return channel.linked_chat.id


app.run()
