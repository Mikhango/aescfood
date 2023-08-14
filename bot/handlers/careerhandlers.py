"""
This file contains functions that take tare about career as a courier
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery


def courier_profile_msg(answers, courier, name : str) -> str:
    """This function returns courier profile text"""

    status = courier[1]

    order_status = answers.COURIERBUSY if status == 0 else \
        answers.COURIERFREE
    coins = courier[3]

    return answers.COURIERPROFILE.format(
                        nick=name, minrub=courier[2], coins=coins, currstatus=order_status)

def send_mainprodile_courier_msg(message : Message, bot : TeleBot, users, answers, markups):
    """Sends main menu message"""

    courier = users.getcourier(message.chat.id)

    if courier is None:
        bot.send_message(message.chat.id, answers.COURIERREG,
                        reply_markup=markups.COURIERREGMARKUP)
        return

    status = courier[1]
    change_status_markup = markups.COURIERFREEMARKUP if status == 0 else \
        markups.COURIERBUSYMARKUP

    bot.send_message(message.chat.id,
                    courier_profile_msg(answers, courier, message.from_user.first_name),
                    reply_markup=change_status_markup, parse_mode="Markdown")

class Career:
    """Class with courier handlers"""

    def couriermain(self, message : Message, bot : TeleBot, users, answers, markups):
        """This file shows user couer profile"""

        send_mainprodile_courier_msg(message, bot, users, answers, markups)

    def regcourier(self, callback_data: CallbackQuery, bot : TeleBot, users, answers, markups):
        """This function registrate user as a courier"""

        try:
            users.addcourier(callback_data.message.chat.id)
        except ValueError:
            bot.send_message(callback_data.message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.edit_message_text(answers.COURIERREGSUCCESS,
                            callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=markups.EMPTYINL)
        send_mainprodile_courier_msg(callback_data.message, bot, users, answers, markups)

    def editcourierstatus(self, callback_data: CallbackQuery, bot : TeleBot, \
                          users, answers, markups):
        """This function edits courier status of user"""

        try:
            users.changecourierstatus(callback_data.message.chat.id)
        except ValueError:
            bot.send_message(callback_data.message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return

        status = users.getcourier(callback_data.message.chat.id)[1]

        change_status_markup = markups.COURIERFREEMARKUP if status == 0 else \
            markups.COURIERBUSYMARKUP
        courier = users.getcourier(callback_data.message.chat.id)

        bot.edit_message_text(courier_profile_msg(answers, courier, \
                                                  callback_data.from_user.first_name),
                            callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=change_status_markup, parse_mode="Markdown")

    def getcourierprice(self, callback_data: CallbackQuery, bot : TeleBot, \
                        answers, states, markups):
        """This function gets courier min price"""

        bot.edit_message_text(answers.COURIERMINPRICE,
                            callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=markups.EMPTYINL)
        bot.set_state(callback_data.from_user.id, states.courierprice, \
                      callback_data.message.chat.id)

    def editprice(self, message : Message, bot : TeleBot, users, answers, markups):
        """This function edits courier price"""

        try:
            users.editcourierprice(message.chat.id, int(message.text))
        except ValueError:
            bot.send_message(message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.send_message(message.chat.id, answers.PROFILEEDITED)
        bot.delete_state(message.from_user.id, message.chat.id)
        send_mainprodile_courier_msg(message, bot, users, answers, markups)

    def errorprice(self, message : Message, bot : TeleBot, users, answers, markups):
        """Check if price correct"""

        bot.send_message(message.chat.id, answers.UNCORRECTPRICE,
                        reply_markup=markups.BASEMARKUP)
        bot.delete_state(message.from_user.id, message.chat.id)
        send_mainprodile_courier_msg(message, bot, users, answers, markups)
