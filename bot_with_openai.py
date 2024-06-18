from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import openai
import logging

load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#configure logging
logging.basicConfig(level=logging.INFO)

openai.api_key = OPENAI_API_KEY

#Intilize bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


class Reference:
    def __init__(self) -> None:
        self.response = ""


reference = Reference()


#To clear the messages
def clear_past():
    reference.response = ""


@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    To clear the messages use /clear
    :param message:
    :return:
    """
    clear_past()
    await message.answer("I've cleared all your messages.")


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """This handler receives messages with `/start` or  `/help `command

    Args:
        message (types.Message): _description_
    """
    await message.reply("Hi\nI am a Chat Bot! Created by Nikhil Kumar Reddy . How can i assist you?")


@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Nikhil Kumar Reddy  Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    Thanks for Using Nikhil Kumar Reddy BOT:)
    """
    await message.reply(help_command)

MODEL_NAME = "gpt-3.5-turbo"
@dp.message_handler()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")

    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)