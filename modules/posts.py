import logging
import random
from asyncio import sleep
from pyrogram.errors import SlowmodeWait, ChannelPrivate


def reply(func):
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except SlowmodeWait as sw:
            if sw.x > 30:
                logging.info(f'Script wont sleep {sw.x}s - >30s ({sw})')
                return
            logging.warning(f'Sleeping {sw.x}s due to {sw}')
            await sleep(sw.x)
            await func(*args, **kwargs)
        await sleep(0.25)

    return wrapper


class TextPost:
    def __init__(self, text):
        self.text = text

    @reply
    async def reply_to(self, message):
        await message.reply_text(self.text)


class PicturePost(TextPost):
    def __init__(self, picture, text=None):
        self.picture = picture
        self.text = text

    @reply
    async def reply_to(self, message):
        await message.reply_photo(self.picture, caption=self.text)


class RandomPost:

    def __init__(self, *args):
        self.posts = args

    async def reply_to(self, message):
        await random.choice(self.posts).reply_to(message)


class DelayedPost:

    def __init__(self, delay=10, *args):
        self.posts = args
        self.delay = delay

    async def reply_to(self, message):
        logging.warning(f"Sleeping {self.delay}s to send delayed post")
        await sleep(self.delay)
        for post in self.posts:
            await post.reply_to(message)


class StickerPost:
    def __init__(self, sticker_id):
        self.sticker_id = sticker_id

    @reply
    async def reply_to(self, message):
        await message.reply_sticker(self.sticker_id)
