"""
This file contains functions that take tare about career as a courier
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery

def couriermain(message : Message, bot : TeleBot, users, ansmsg):
    """This file shows user couer profile"""

    status = users.getuser(message.chat.id)[1]

    if status == -1:
        bot.send_message(message.chat.id, ansmsg['answers']['COURIERREG'],
                         reply_markup=ansmsg['markups']['COURIERREGMARKUP'])
        return

    order_status = ansmsg['answers']['COURIERBUSY'] if status == 0 else \
        ansmsg['answers']['COURIERFREE']
    change_status_markup = ansmsg['markups']['COURIERFREEMARKUP'] if status == 0 else \
        ansmsg['markups']['COURIERBUSYMARKUP']
    coins = users.getuser(message.chat.id)[4]

    bot.send_message(message.chat.id, ansmsg['answers']['COURIERPROFILE'].format(
                        nick=message.from_user.first_name, coins=coins, currstatus=order_status),
                        reply_markup=change_status_markup, parse_mode="Markdown")

def regcourier(callback_data: CallbackQuery, bot : TeleBot, users, ansmsg):
    """This function registrate user as a courier"""

    try:
        users.edituser("status", 0, callback_data.message.chat.id)
    except ValueError:
        bot.send_message(callback_data.message.chat.id, ansmsg['answers']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return

    bot.edit_message_text(ansmsg['answers']['COURIERREGSUCCESS'],
                          callback_data.from_user.id, callback_data.message.message_id,
                          reply_markup=ansmsg['markups']['EMPTYINL'])

def editcourierstatus(callback_data: CallbackQuery, bot : TeleBot, users, ansmsg):
    """This function edits courier status of user"""

    status = users.getuser(callback_data.message.chat.id)[1]

    try:
        users.edituser("status", int(not status), callback_data.message.chat.id)
    except ValueError:
        bot.send_message(callback_data.message.chat.id, ansmsg['answers']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return

    status = 0 if status == 1 else 1

    order_status = ansmsg['answers']['COURIERBUSY'] if status == 0 else \
        ansmsg['answers']['COURIERFREE']
    change_status_markup = ansmsg['markups']['COURIERFREEMARKUP'] if status == 0 else \
        ansmsg['markups']['COURIERBUSYMARKUP']
    coins = users.getuser(callback_data.message.chat.id)[4]

    bot.edit_message_text(ansmsg['answers']['COURIERPROFILE'].format(
                        nick=callback_data.from_user.first_name, coins=coins,
                        currstatus=order_status),
                        callback_data.from_user.id, callback_data.message.message_id,
                        reply_markup=change_status_markup, parse_mode="Markdown")
