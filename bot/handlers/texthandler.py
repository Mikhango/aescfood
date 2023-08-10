"""
This file contains text handler
"""

from telebot import TeleBot
from telebot.types import Message


def bad_request(message: Message, bot: TeleBot, ansmsg):
    """
    This function answer on any requests, that weren't accepted
    by other functions
    """

    bot.send_message(message.chat.id, ansmsg['answers']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
