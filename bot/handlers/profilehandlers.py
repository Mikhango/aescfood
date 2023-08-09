"""
This file contain functions that will get user profile
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery


def myprofile(message : Message, bot : TeleBot, users, ansmsg):
    """This function gets user profile"""

    user = ()

    try:
        user = users.getuser(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['answers']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return

    bot.send_message(message.chat.id, ansmsg['answers']['PROFILE'].format(
        nick=message.from_user.first_name, number=user[2], room=user[3]),
                     reply_markup=ansmsg['markups']['PROFILEMARKUP'], parse_mode= 'Markdown')

def changenumber(callback_data: CallbackQuery, bot : TeleBot, users, ansmsg, checkers):
    """This function allows user to change his number"""

    bot.edit_message_text(ansmsg['answers']['EDITNUMBER'],
                          callback_data.from_user.id, callback_data.message.message_id,
                          reply_markup=ansmsg['markups']['EMPTYINL'])
    bot.register_next_step_handler(callback_data.message, enternumber, bot=bot,
                                   users=users, ansmsg=ansmsg, checkers=checkers)

def changeroom(callback_data: CallbackQuery, bot : TeleBot, users, ansmsg):
    """This function allows user to change his room number"""

    bot.edit_message_text(ansmsg['answers']['EDITROOM'],
                          callback_data.from_user.id, callback_data.message.message_id,
                          reply_markup=ansmsg['markups']['EMPTYINL'])
    bot.register_next_step_handler(callback_data.message, enterroom, bot=bot,
                                   users=users, ansmsg=ansmsg)

def enterroom(message : Message, bot : TeleBot, users, ansmsg):
    """This function edits user room"""

    try:
        users.edituser("room", message.text, message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['answers']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return
    bot.send_message(message.chat.id, ansmsg['answers']['PROFILEEDITED'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])

def enternumber(message : Message, bot : TeleBot, users, ansmsg, checkers):
    """This function edits user number"""

    if not checkers.checknum(message.text):
        bot.send_message(message.chat.id, ansmsg['answers']['PHONEWRONG'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return

    try:
        users.edituser("number", message.text, message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['answers']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return
    bot.send_message(message.chat.id, ansmsg['answers']['PROFILEEDITED'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
