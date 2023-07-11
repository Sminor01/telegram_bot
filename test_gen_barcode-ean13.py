from pylibdmtx.pylibdmtx import encode
from PIL import Image
import telebot
from datetime import datetime
from telebot.apihelper import ApiException
from time import time, sleep
import logging
import random
import barcode
from barcode import EAN13
from barcode.writer import ImageWriter
def generate_ean13():
    digits = [random.randint(0, 9) for _ in range(12)]

    odd_sum = sum(digits[0::2])
    even_sum = sum(digits[1::2])
    control_sum = (odd_sum * 3 + even_sum) % 10
    control_sum = (10 - control_sum) if control_sum != 0 else 0

    barcode = digits + [control_sum]

    barcode_str = ''.join(map(str, barcode))

    return barcode_str


barcode = generate_ean13()
print(barcode)

data = barcode
barcode_gen = EAN13(data)
with open("EAN-13.png", "wb") as f:
    EAN13(barcode, writer=ImageWriter()).write(f)
