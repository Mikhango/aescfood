"""
This file contains text handler
"""

from telebot import TeleBot
from telebot.types import Message


BAD_REQUEST = "Я не понимаю😢"


def text_answer(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    bot.send_message(message.chat.id, BAD_REQUEST)
