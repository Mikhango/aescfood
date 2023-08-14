"""
This file contains text handler
"""

from telebot import TeleBot
from telebot.types import Message


def bad_request(message: Message, bot: TeleBot, answers, markups):
    """
    This function answer on any requests, that weren't accepted
    by other functions
    """

    bot.send_message(message.chat.id, answers.BADREQUEST,
                     reply_markup=markups.BASEMARKUP)
