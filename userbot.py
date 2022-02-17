#  _____  _       _              _                 
# |  __ \| |     | |            (_)                
# | |__) | |_   _| |_ ___  _ __  _ _   _ _ __ ___  
# |  ___/| | | | | __/ _ \| '_ \| | | | | '_ ` _ \ 
# | |    | | |_| | || (_) | | | | | |_| | | | | | |
# |_|    |_|\__,_|\__\___/|_| |_|_|\__,_|_| |_| |_|


from asyncio import sleep
from datetime import datetime
from pyrogram import Client, filters

app: Client = Client("my_account", workers=1)
spam_text = '1st'
send_chat = None


with app:
    print('Started! Wait for a new message to set up the bot.')


@app.on_message(filters.channel)
async def spam(_, message):
    if (message.edit_date is None or (datetime.utcfromtimestamp(message.edit_date) - datetime.utcfromtimestamp(
            message.date)).total_seconds() > 5):
        return

    linked = await get_linked(message)
    await sleep(0.25)

    await init_sender(linked)
    await sleep(0.25)

    msg = await app.get_history(linked, limit=1)
    await sleep(0.25)

    await msg[0].reply_text(spam_text)
    await sleep(0.25)

    print("Answered to: " + message.chat.title)


async def init_sender(_chat):
    global send_chat
    if not send_chat:
        chats = await app.get_send_as_chats(_chat)
        print("Available chats:")
        for index, chat in enumerate(chats):
            chat_name = chat.title if chat.first_name is None else chat.first_name
            print(str(index) + ": " + chat_name)
        answer = int(input("Write ID of chat and press Enter: "))
        send_chat = chats[answer].id


async def get_linked(msg):
    channel = await app.get_chat(msg.sender_chat.id)
    return channel.linked_chat.id


app.run()
