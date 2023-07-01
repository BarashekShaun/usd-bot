import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import token, user_id
from main import get_currency

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ['USD']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Курс на сегодня", reply_markup=keyboard)


@dp.message_handler(Text(equals='USD'))
async def get_usd(message: types.Message):
    with open("currency_base.json") as file:
        new_dict = json.load(file)

    currency = f"Сегодня {new_dict['date']}\n" \
               f"Курс доллара США по ЦБ: <b>{new_dict['USD']}</b>"


    await message.answer(currency)


async def update_every_day():
    while True:
        update = get_currency()
        with open("currency_base.json") as file:
            new_dict = json.load(file)

        if float(new_dict['USD'].replace(',', '.')) < 40:
            big_news = f"ОХУЕТЬ, ДОЛЛАР НИЖЕ 40!"
            await bot.send_message(user_id, big_news)

        else:
            await bot.send_message(user_id, "Доллар все еще не 40...", disable_notification=True)

        await asyncio.sleep(86400)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(update_every_day())
    executor.start_polling(dp)


