"""
This file contains functions that take tare about career as a courier
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery


def courier_profile_msg(ansmsg: dict, courier, name : str) -> str:
    """This function returns courier profile text"""

    status = courier[1]

    order_status = ansmsg['answers']['COURIERBUSY'] if status == 0 else \
        ansmsg['answers']['COURIERFREE']
    coins = courier[3]

    return ansmsg['answers']['COURIERPROFILE'].format(
                        nick=name, minrub=courier[2], coins=coins, currstatus=order_status)


def couriermain(message : Message, bot : TeleBot, users, ansmsg):
    """This file shows user couer profile"""

    courier = users.getcourier(message.chat.id)

    if courier is None:
        bot.send_message(message.chat.id, ansmsg['answers']['COURIERREG'],
                         reply_markup=ansmsg['markups']['COURIERREGMARKUP'])
        return

    status = courier[1]
    change_status_markup = ansmsg['markups']['COURIERFREEMARKUP'] if status == 0 else \
        ansmsg['markups']['COURIERBUSYMARKUP']

    bot.send_message(message.chat.id,
                     courier_profile_msg(ansmsg, courier, message.from_user.first_name),
                     reply_markup=change_status_markup, parse_mode="Markdown")

def regcourier(callback_data: CallbackQuery, bot : TeleBot, users, ansmsg):
    """This function registrate user as a courier"""

    try:
        users.addcourier(callback_data.message.chat.id)
    except ValueError:
        bot.send_message(callback_data.message.chat.id, ansmsg['answers']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return

    bot.edit_message_text(ansmsg['answers']['COURIERREGSUCCESS'],
                          callback_data.from_user.id, callback_data.message.message_id,
                          reply_markup=ansmsg['markups']['EMPTYINL'])

def editcourierstatus(callback_data: CallbackQuery, bot : TeleBot, users, ansmsg):
    """This function edits courier status of user"""

    try:
        users.changecourierstatus(callback_data.message.chat.id)
    except ValueError:
        bot.send_message(callback_data.message.chat.id, ansmsg['answers']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return

    status = users.getcourier(callback_data.message.chat.id)[1]

    change_status_markup = ansmsg['markups']['COURIERFREEMARKUP'] if status == 0 else \
        ansmsg['markups']['COURIERBUSYMARKUP']
    courier = users.getcourier(callback_data.message.chat.id)

    bot.edit_message_text(courier_profile_msg(ansmsg, courier, callback_data.from_user.first_name),
                        callback_data.from_user.id, callback_data.message.message_id,
                        reply_markup=change_status_markup, parse_mode="Markdown")

def getcourierprice(callback_data: CallbackQuery, bot : TeleBot, users, ansmsg, checkers):
    """This function gets courier min price"""

    bot.edit_message_text(ansmsg['answers']['COURIERMINPRICE'],
                        callback_data.from_user.id, callback_data.message.message_id,
                        reply_markup=ansmsg['markups']['EMPTYINL'])
    bot.register_next_step_handler(message=callback_data.message, callback=editprice, bot=bot,
                                        users=users, ansmsg=ansmsg, checkers=checkers)

def editprice(message : Message, bot : TeleBot, users, ansmsg, checkers):
    """This function edits courier price"""

    if not checkers.checkprice(int(message.text)):
        bot.send_message(message.chat.id, ansmsg['answers']['UNCORRECTPRICE'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        bot.register_next_step_handler(message=message, callback=editprice, bot=bot,
                                        users=users, ansmsg=ansmsg, checkers=checkers)
        return

    try:
        users.editcourierprice(message.chat.id, message.text)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['answers']['BADREQUEST'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return

    status = users.getcourier(message.chat.id)[1]

    change_status_markup = ansmsg['markups']['COURIERFREEMARKUP'] if status == 0 else \
        ansmsg['markups']['COURIERBUSYMARKUP']
    courier = users.getcourier(message.chat.id)

    bot.send_message(message.chat.id, ansmsg['answers']['PROFILEEDITED'])
    bot.send_message(message.chat.id,
                     courier_profile_msg(ansmsg, courier, message.from_user.first_name),
                     reply_markup=change_status_markup, parse_mode="Markdown")
