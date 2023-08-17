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

def send_mainprofile_courier_msg(message : Message, bot : TeleBot, users, answers, markups, name):
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
                    courier_profile_msg(answers, courier, name),
                    reply_markup=change_status_markup, parse_mode="Markdown")

def orders_courier(message : Message, bot : TeleBot, users, answers, markups):
    """Sends courier's orders"""

    orders = []

    try:
        orders = users.getcourierorders(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, answers.BADREQUEST,
                    reply_markup=markups.BASEMARKUP)
        return

    msg = answers.ORDERSTOOK

    for order in orders:
        try:
            user = users.getuser(order[1])
        except ValueError:
            bot.send_message(message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return
        msg += answers.ORDERCOURIER.\
        format(id=order[0], name=order[2], number=user[1], \
               room=order[5], price=order[6], comment=order[7])

    if orders == []:
        msg += "У вас нет заказов"

    bot.send_message(message.chat.id, msg,
                    reply_markup=markups.MYORDERSCOURIER, parse_mode="Markdown")


class Career:
    """Class with courier handlers"""

    def couriermain(self, message : Message, bot : TeleBot, users, answers, markups):
        """This file shows user couer profile"""

        send_mainprofile_courier_msg(message, bot, users, answers, markups, \
                                     message.from_user.first_name)
        bot.delete_state(message.from_user.id, message.chat.id)

    def orderscouriermain(self, callback_data: CallbackQuery, bot : TeleBot, \
                          users, answers, markups):
        """Sends all orders of courier"""

        orders_courier(callback_data.message, bot, users, answers, markups)

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
        send_mainprofile_courier_msg(callback_data.message, bot, users, answers, markups, \
                                     callback_data.from_user.first_name)

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
        send_mainprofile_courier_msg(message, bot, users, answers, markups, \
                                     message.from_user.first_name)

    def errorprice(self, message : Message, bot : TeleBot, users, answers, markups):
        """Check if price correct"""

        bot.send_message(message.chat.id, answers.UNCORRECTPRICE,
                        reply_markup=markups.BASEMARKUP)
        bot.delete_state(message.from_user.id, message.chat.id)
        send_mainprofile_courier_msg(message, bot, users, answers, markups, \
                                     message.from_user.first_name)

    def takeorder(self, callback_data: CallbackQuery, bot : TeleBot, \
                        answers, users, markups):
        """Lets user take an order"""

        chat_id = callback_data.message.chat.id

        if len(users.getcourierorders(chat_id)) >= 2:
            bot.send_message(callback_data.from_user.id, answers.LIMITORDERS,
                        reply_markup=markups.BASEMARKUP)
            return

        order_id = int(callback_data.data.split('-')[1])
        client_id = None

        if not users.checkorderid(order_id) or users.checkordercourier(order_id):
            bot.edit_message_text(answers.ERRORTOOKORDER,
                            callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=markups.EMPTYINL)
            return

        order = None
        number_courier = None

        try:
            users.addordercourier(order_id, chat_id, \
                                  callback_data.from_user.first_name)
            order = users.getorder(order_id)
            client_id = order[1]
            number_courier = users.getuser(chat_id)[1]
        except ValueError:
            bot.send_message(chat_id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.edit_message_text(answers.TOOKORDERCOURIER,
                            callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=markups.EMPTYINL)
        bot.send_message(client_id, answers.TOOKORDERPUSH.format(id=order_id, \
                         name=callback_data.from_user.first_name, number=number_courier), \
                            parse_mode="Markdown")

    def didordercourier(self, callback_data: CallbackQuery, bot : TeleBot,
                 users, answers, markups, states):
        """This function starts deleting order"""

        if len(users.getcourierorders(callback_data.from_user.id)) == 0:
            bot.send_message(callback_data.from_user.id, answers.NOORDERS,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.edit_message_reply_markup(callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=markups.EMPTYINL)
        bot.send_message(callback_data.from_user.id, answers.ORDERCOURIERGETID)
        bot.set_state(callback_data.from_user.id, states.courierdelord, \
                      callback_data.message.chat.id)

    def getiddidord(self, message : Message, bot : TeleBot, users, answers, markups):
        """This function gets id of deleting order and deletes it"""

        order = None

        try:
            order = users.getorder(int(message.text))
            users.editcouriermoney(message.chat.id, order[6])
            users.delorder(int(message.text))
        except ValueError:
            bot.send_message(message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.send_message(message.chat.id, answers.ORDERDIDSUCCESS,
                        parse_mode="Markdown")
        bot.send_message(order[1], answers.ORDERDIDPUSH.format(id=order[0]),
                        parse_mode="Markdown")
        bot.delete_state(message.from_user.id, message.chat.id)
        orders_courier(message, bot, users, answers, markups)

    def badcourierorder(self, message : Message, bot : TeleBot, answers, markups, users):
        """If user haven't this order"""

        bot.send_message(message.chat.id, answers.BADORDER, parse_mode="Markdown")
        bot.delete_state(message.from_user.id, message.chat.id)
        orders_courier(message, bot, users, answers, markups)
