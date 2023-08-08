"""
This file contains text handler
"""

from telebot import TeleBot
from telebot.types import Message


def bad_request(message: Message, bot: TeleBot, users, ansmsg):
    """
    This function answer on any requests, that weren't accepted
    by other functions
    """

    if not users.checkuser(message.chat.id):
        bot.send_message(message.chat.id, ansmsg['buttons']['DOESNTREG'])
        return

    bot.send_message(message.chat.id, ansmsg['buttons']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
