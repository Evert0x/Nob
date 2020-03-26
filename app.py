# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
logging.basicConfig()
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

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1



from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def hehe(input):
    meme = Image.open(input).convert('RGBA').resize((208, 208))
    #input = Image.open('meme.jpg', 'r').convert('RGBA')
    #meme = input.resize((208, 208))

    img = Image.open('resources/image.jpg', 'r')
    #meme = Image.new('RGBA', (208, 208), (255, 255, 255, 255))
    meme = meme.rotate(3.8, resample=Image.BICUBIC, expand=True)
    img.paste(meme, (30, 290), meme)
    #img.save("out.png")
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
        lines.append(string[i:i+every])
    return '\n'.join(lines)

def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            print(update.message)
            cap = ""
            if update.message.caption:
                cap = update.message.caption.lower()
            elif update.message.text:
                cap = update.message.text.lower()


            if cap in ["nob", "@nobbiebot", "norbert"] or ".nob" in cap:
                pass
            else:
                return


            if update.message.text:
                t = update.message.text.replace(".nob", "").strip()
                t = insert_newlines(t)

                img = Image.new('RGBA', (208, 208), (0, 0, 0))
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/freefont/FreeMono.ttf", 28,
                    encoding="unic")                # draw.text((x, y),"Sample Text",(r,g,b))
                draw.text((0, 0), t, (255, 255, 255), font=font)
                bytes = io.BytesIO()
                w = io.BufferedWriter(bytes)
                img.save(w, format="PNG")
                bytes.seek(0)
                byteImg = bytes.read()
                dataBytesIO = io.BytesIO(byteImg)
                try:
                    img = hehe(bytes)

                    imgByteArr = io.BytesIO()
                    img.save(imgByteArr, format='PNG')

                    imgByteArr.seek(0)
                    update.message.reply_photo(photo=imgByteArr)
                except IOError as e:
                    print("error")
                    print(e)

            elif update.message.photo:
                photo = update.message.photo[0]
                print("meme")
                new_file = bot.getFile(photo.file_id)
                bytes = io.BytesIO()
                w = io.BufferedWriter(bytes)
                new_file.download(out=w)
                bytes.seek(0)
                byteImg = bytes.read()
                dataBytesIO = io.BytesIO(byteImg)
                # Non test code
                #dataBytesIO = io.BytesIO(dataBytesIO)

                #r = io.BufferedReader(bytes)

                try:
                    img = hehe(dataBytesIO)

                    imgByteArr = io.BytesIO()
                    img.save(imgByteArr, format='PNG')

                    imgByteArr.seek(0)
                    update.message.reply_photo(photo=imgByteArr)
                except IOError as e:
                    print("error")
                    print(e)

            #update.message.reply_text(update.message.text)


if __name__ == '__main__':
    main()