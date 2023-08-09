"""
This file will register functions as handlers
"""

from telebot import TeleBot

from bot.answers import buttons, callbacks

from bot.handlers.registercheck import checkreg
from bot.handlers.reghandlers import start
from bot.handlers.texthandler import bad_request
from bot.handlers.profilehandlers import myprofile, changenumber, changeroom

def register_handlers(bot : TeleBot, users):
    """This function register all handlers in necessary order"""

    bot.register_message_handler(callback=start, commands=["start"], pass_bot=True)
    bot.register_message_handler(callback=checkreg,
                                 func=lambda msg: not users.checkuser(msg.chat.id),
                                 pass_bot=True)

    bot.register_message_handler(callback=myprofile, regexp=buttons["PROFILEBTN"], pass_bot=True)
    bot.register_message_handler(callback=bad_request, pass_bot=True)

def register_callback_handlers(bot : TeleBot):
    """This function register all callback handlers in necessary order"""
    bot.register_callback_query_handler(callback=changenumber,
                                        func=lambda c: c.data == callbacks["CALLBACKNUMBER"],
                                        pass_bot=True)
    bot.register_callback_query_handler(callback=changeroom,
                                        func=lambda c: c.data == callbacks["CALLBACKROOM"],
                                        pass_bot=True)
