# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging

logging.basicConfig()

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import telegram
import io
from telegram.error import NetworkError, Unauthorized
from time import sleep

update_id = None


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('175945840:AAH6VuIrnDYVL9nU6wa-yLHCZNGLCHTejoI')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


memes = [
    {
        "meme_size": (208, 208),
        "resource": 'resources/image.jpg',
        "rotate": 3.8,
        "location": (30, 290)
    },
    {
        "meme_size": (270, 370),
        "resource": 'resources/trump.jpg',
        "rotate": -3,
        "location": (340, 209)
    }
]

def merge_meme(input):
    hehe = memes[0]
    meme = Image.open(input).convert('RGBA').resize(hehe["meme_size"])
    img = Image.open(hehe["resource"], 'r')
    meme = meme.rotate(hehe["rotate"], resample=Image.BICUBIC, expand=True)
    img.paste(meme, hehe["location"], meme)
    # img.save("out.png")
    return img


def insert_newlines(string, every=10):
    import textwrap
    lines = textwrap.wrap(string, every)
    # then use either
    return '\n'.join(lines)
    # or
    '\n'.join(lines)

    lines = []
    for i in range(0, len(string), every):
        lines.append(string[i:i + every])
    return '\n'.join(lines)


def handle_photo(bot, photo):
    new_file = bot.getFile(photo.file_id)
    bytes = io.BytesIO()
    w = io.BufferedWriter(bytes)
    new_file.download(out=w)
    bytes.seek(0)
    return w, bytes

def handle_text(bot, text):
    t = insert_newlines(text)

    img = Image.new('RGBA', (208, 208), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/freefont/FreeMono.ttf", 28,
        encoding="unic")  # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((0, 0), t, (0, 0, 0), font=font)
    bytes = io.BytesIO()
    w = io.BufferedWriter(bytes)
    img.save(w, format="PNG")
    bytes.seek(0)
    return w, bytes

def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if not update.message:
            return

        res = None
        if update.message.photo:
            trigger = update.message.caption or ""
            if not trigger.lower() in ["nob", "@nobbiebot", "norbert", ".nob"]:
                return
            w, res = handle_photo(bot, update.message.photo[0])

        elif update.message.text:
            t = update.message.text.lower()
            if "relatie" in t:
                update.message.reply_text("""Hey ☺️ ik heb even na zitten denken over bepaalde dingen en ik merk dat ik een beetje in de knoop zit met deze dingen te verwerken. Je bent een leuke jongen die ook echt een leuke meid verdient alleen denk ik niet dat ik die meid kan zijn. Ik heb het super leuk met je gehad maar ik wil me graag eerst op mezelf gaan focussen nu. Ik wil eerlijk tegen je zijn en je niet aan het lijntje houden. Ik hoop dat je dit begrijpt 🤗""")
                return
            if "morgen" in t:
                update.message.reply_text("""https://open.spotify.com/track/1WaaCM1vJv6qDr8jYIEsZA?si=xUC0Q5VVSaay1ttTGpnPOg""", disable_web_page_preview=True)
                return
            if not t.startswith(".nob"):
                return
            t = t.replace(".nob", "").strip()
            w, res = handle_text(bot, t)

        if not res:
            return

        try:
            img = merge_meme(res)

            imgByteArr = io.BytesIO()
            img.save(imgByteArr, format='PNG')

            imgByteArr.seek(0)
            update.message.reply_photo(photo=imgByteArr)
        except IOError as e:
            print("error")
            print(e)

if __name__ == '__main__':
    main()
