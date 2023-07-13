from pylibdmtx.pylibdmtx import encode
from PIL import Image
import telebot
from datetime import datetime
from telebot.apihelper import ApiException
from time import time, sleep
import logging
import barcode
from pyzbar import pyzbar
import cv2

#create bot with botfather#
TOKEN = '#your token#'

bot = telebot.TeleBot(TOKEN)

# слушаем сообщениея
def listener(messages):
    for m in messages:
        print(
            f'[{datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")}] {m.from_user.first_name} [{m.from_user.username} : {m.from_user.id}] [{m.chat.id}]:{m.text if m.text else m.content_type} : {m.chat.type}')

bot.set_update_listener(listener)
telebot.logger.setLevel(logging.DEBUG)



@bot.message_handler(commands=['start'])
def start_cmd(m):
    bot.send_message(m.chat.id, 'Привет!')


@bot.message_handler(func=lambda m: len(m.text.splitlines()[0]) == 27)
def msg_text(m):
    GS = chr(29)
    for sgtin in m.text.split():
        if len(sgtin) != 27:
            continue
        datamatrix = f'01{sgtin[:14]}21{sgtin[14:]}{GS}91EE06{GS}92ZnwHSt0au2BP3Ps0qnrcZv2XWpM8TBYry2pHZ+RObyM='
        encoded = encode(datamatrix.encode('utf-8'))
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        img.save('dmtx.png')

        bot.send_photo(m.chat.id, photo=open('dmtx.png', 'rb'), caption=sgtin)

def polling(bot_instance):
    bot.remove_webhook()
    if bot_instance.skip_pending:
        lid = bot_instance.get_updates()[-1].update_id
    else:
        lid = 0
    while 1:
        try:
            updates = bot_instance.get_updates(lid + 1, 50)
            if len(updates) > 0:
                lid = updates[-1].update_id
                bot_instance.process_new_updates(updates)
        except ApiException as api:
            print(api)
        except Exception as e:
            now = int(time())
            while 1:
                error_text = 'Дичь:\n%s' % (
                    str(e) if len(str(e)) < 3600 else str(e)[:3600])
                try:
                    offline = int(time()) - now
                    bot_instance.send_message(
                        165584881, error_text + '\nБот был оффлайн %s секунд' % offline)
                    break
                except ApiException as err:
                    sleep(0.25)
                    print(err)

try:
    print('Имя бота:[%s]' % bot.get_me().username)
except ApiException as a:
    print(a)
    exit(1)

try:
    print('start')
except ApiException:
    exit(1)
print('Начали')
polling(bot)
