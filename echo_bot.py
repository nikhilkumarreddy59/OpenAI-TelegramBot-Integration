from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging

load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
logging.basicConfig(level=logging.INFO)

#initilize the bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def command_handler(message: types.Message):
    """
    This function receives message with /start and /help commands
    :param message:
    :return:
    """

    await message.reply("Hi!\n I am an Nikhil  Echo Bot!\n Powered by Aiogram")

@dp.message_handler()

async def echo_handler(message: types.Message):
    """
    This function receives message with /echo commands
    :param message:
    :return:
    """
    await message.reply(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)