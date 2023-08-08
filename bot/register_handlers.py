"""
This file will register functions as handlers
"""

from telebot import TeleBot

from bot.handlers.reghandlers import start
from bot.handlers.texthandler import bad_request


def register_handlers(bot : TeleBot, users):
    """This function register all handlers in necessary order"""

    bot.register_message_handler(callback=start, commands=["start"], pass_bot=bot)
    bot.register_message_handler(callback=bad_request, pass_bot=bot)
