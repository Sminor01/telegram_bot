from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from pybarcodes import EAN13
from io import BytesIO

bot = Bot(token="#your token#")
dp = Dispatcher(bot)


def generate_ean13(digits):
    odd_sum = sum(digits[0::2])
    even_sum = sum(digits[1::2])
    control_sum = (odd_sum * 3 + even_sum) % 10
    control_sum = (10 - control_sum) if control_sum != 0 else 0

    barcode = digits + [control_sum]

    barcode_str = ''.join(map(str, barcode))

    return barcode_str


def generate_image_barcode(code):
    barcode = generate_ean13(code)
    data = barcode
    barcode_gen = EAN13(data)
    file = BytesIO()
    file.name = 'EAN-13.png'
    barcode_gen.image.save(file, 'PNG')
    file.seek(0)
    return file


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Отправьте 13 цифр от 0 до 9.")


@dp.message_handler()
async def generate(message: types.Message):
    if message.text.isnumeric() and len(message.text) == 13:
        digits = [int(s) for s in message.text]
        photo = InputFile(generate_image_barcode(digits))
        await message.answer_photo(photo)
    else:
        await message.answer("Отправьте 13 цифр от 0 до 9.")


if __name__ == "__main__":
    executor.start_polling(dp)

