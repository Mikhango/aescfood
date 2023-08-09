"""
This file takes care about user was registered
"""

from telebot import TeleBot
from telebot.types import Message


def checkreg(message: Message, bot: TeleBot, ansmsg):
    """
    This function check was user registered or not
    """

    bot.send_message(message.chat.id, ansmsg['answers']['DOESNTREG'])
