"""
This file takes care about user was registered
"""

from telebot import TeleBot
from telebot.types import Message


def checkreg(message: Message, bot: TeleBot, answers):
    """
    This function check was user registered or not
    """

    bot.send_message(message.chat.id, answers.DOESNTREG)
