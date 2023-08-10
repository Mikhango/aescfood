"""
This file contain functions that will register user
"""

from telebot import TeleBot
from telebot.types import Message


def start(message : Message, bot : TeleBot, users, ansmsg, checkers):
    """This function answer on a /start command"""

    try:
        users.adduser(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['answers']['BADREQUESTREG'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return

    bot.send_message(message.chat.id, ansmsg['answers']['STARTMSG'])
    bot.send_message(message.chat.id, ansmsg['answers']['TELEPHONE'])
    bot.register_next_step_handler(message=message, callback=getnumber, bot=bot, users=users,
                                   ansmsg = ansmsg, checkers=checkers)

def getnumber(message : Message, bot : TeleBot, users, ansmsg, checkers):
    """This function gets number of user"""

    if not checkers.checknum(message.text):
        bot.send_message(message.chat.id, ansmsg['answers']['PHONEWRONG'])
        bot.register_next_step_handler(message=message, callback=getnumber, bot=bot,
                                        users=users, ansmsg=ansmsg, checkers=checkers)
        return

    try:
        users.editusernumber(message.chat.id, message.text)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['answers']['BADREQUESTREG'])
        return

    bot.send_message(message.chat.id, ansmsg['answers']['ROOM'])
    bot.register_next_step_handler(message=message, callback=getroom, bot=bot, users=users,
                                   ansmsg=ansmsg, checkers=checkers)

def getroom(message : Message, bot : TeleBot, users, ansmsg, checkers):
    """This function gets user's room number"""

    if not checkers.checkroom(message.text):
        bot.send_message(message.chat.id, ansmsg['answers']['ROOMWRONG'])
        bot.register_next_step_handler(message=message, callback=getroom, bot=bot,
                                        users=users, ansmsg=ansmsg, checkers=checkers)
        return

    try:
        users.edituserroom(message.chat.id, message.text)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['answers']['BADREQUESTREG'])
        return

    bot.send_message(message.chat.id, ansmsg['answers']['ENDREG'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
