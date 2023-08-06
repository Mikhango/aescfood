"""
This file contains text handler
"""

from telebot import TeleBot
from telebot.types import Message


BAD_REQUEST = "Я не понимаю😢"


def bad_request(message: Message, bot: TeleBot):
    """
    This function answer on any requests, that weren't accepted
    by other functions
    """
    print(message.text)
    bot.send_message(message.chat.id, BAD_REQUEST)
