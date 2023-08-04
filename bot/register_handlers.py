"""
This file will register all functions as handlers
"""

from telebot import TeleBot

from bot.handlers.texthandler import text_answer


def register_handlers(bot : TeleBot):
    """This function register all handlers in necessary order"""

    bot.register_message_handler(callback=text_answer, pass_bot=bot)
