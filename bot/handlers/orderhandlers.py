"""
This file contain functions that
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery, \
InlineKeyboardButton, InlineKeyboardMarkup
from telebot.apihelper import ApiTelegramException

def form_order(answers, userid : int, courier : str, number : str, room : str, \
              price : int, comment : str):
    """This function formats order message"""

    if courier == "":
        courier = answers.FINDCOURIER
    if number == "":
        number = answers.FINDCOURIER

    return answers.ORDERFORMAT.\
        format(id=userid, name=courier, number=number, room=room, price=price, comment=comment)

def msg_orders(message : Message, bot : TeleBot, users, answers,\
                   markups):
    """Formats orders message and send it"""

    orders = []

    try:
        orders = users.getuserorders(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, answers.BADREQUEST,
                    reply_markup=markups.BASEMARKUP)
        return

    msg = answers.ORDERSMAIN

    for order in orders:
        user = None
        try:
            user = users.getuser(order[3])
        except ValueError:
            bot.send_message(message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return
        number = user[1] if order[3] != -1 and user is not None else ""
        msg += form_order(answers=answers, userid=order[0], courier=order[4], number=number,
                        room=order[5], price=order[6], comment=order[7])

    if orders == []:
        msg += "У вас нет заказов"

    bot.send_message(message.chat.id, msg,
                    reply_markup=markups.ACTORDER, parse_mode="Markdown")

def msg_courier_orders(message : Message, bot : TeleBot, users, answers,\
                   markups, callbacks, id_ord):
    """Formats orders message and send it"""

    couriers = None
    order = None

    try:
        couriers = users.getfreecouriers()
        order = users.getorder(id_ord)
    except ValueError:
        bot.send_message(message.chat.id, answers.BADREQUEST,
                    reply_markup=markups.BASEMARKUP)
        return

    msg = answers.NEWORDERCOURIER.\
    format(id=id_ord, name=message.from_user.first_name, \
           room=order[5], price=order[6], comment=order[7])

    btn = InlineKeyboardButton(answers.TAKEORDER, callback_data=\
                               f"{callbacks.CALLBACKTAKEORDER}{id_ord}")
    keyboard = InlineKeyboardMarkup().add(btn)

    for courier in couriers:
        try:
            if courier[2] <= order[6] and courier[0] != message.chat.id:
                bot.send_message(courier[0], msg, reply_markup=keyboard, parse_mode="Markdown")
        except ApiTelegramException:
            continue

class Orders:
    """Orders handlers"""

    def ordersmain(self, message : Message, bot : TeleBot, users, answers,\
                   markups):
        """This function gets current orders"""

        msg_orders(message, bot, users, answers, markups)
        bot.delete_state(message.from_user.id, message.chat.id)

    def createorder(self, callback_data: CallbackQuery, bot : TeleBot, users, answers, \
                     markups, states):
        """This function helps create order"""

        if len(users.getuserorders(callback_data.from_user.id)) >= 2:
            bot.send_message(callback_data.from_user.id, answers.LIMITORDERS,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.edit_message_text(answers.ORDERGETPRICE,
                            callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=markups.EMPTYINL, parse_mode="Markdown")
        bot.set_state(callback_data.from_user.id, states.getordprice, callback_data.message.chat.id)

    def getordprice(self, message : Message, bot : TeleBot, answers, markups, states):
        """This function gets order price"""

        price = int(message.text)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['ordprice'] = price

        bot.send_message(message.chat.id, answers.ORDERGETCOMMENT,
                        reply_markup=markups.EMPTYINL, parse_mode="Markdown")
        bot.set_state(message.from_user.id, states.getordcomm, message.chat.id)

    def incorrectordprice(self, message : Message, bot : TeleBot, answers, markups):
        """Controls price correct"""

        bot.send_message(message.chat.id, answers.UNCORRECTPRICE,
                        reply_markup=markups.EMPTYINL, parse_mode="Markdown")

    def regorder(self, message : Message, bot : TeleBot, users, answers, markups, callbacks):
        """This function gets order comment and regs order"""

        comment = message.text
        id_ord = None

        try:
            client = users.getuser(message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                id_ord = users.addorder(client_id=message.chat.id,
                               client_name=message.from_user.first_name,
                               room=client[2], price=data['ordprice'], comment=comment)
        except ValueError:
            bot.send_message(message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.send_message(message.chat.id, answers.ORDERSUCCESS,
                        reply_markup=markups.EMPTYINL, parse_mode="Markdown")
        bot.delete_state(message.from_user.id, message.chat.id)

        msg_courier_orders(message, bot, users, answers, markups, callbacks, id_ord)

        msg_orders(message, bot, users, answers, markups)

    def delorder(self, callback_data: CallbackQuery, bot : TeleBot,
                 users, answers, markups, states):
        """This function starts deleting order"""

        if len(users.getuserorders(callback_data.from_user.id)) == 0:
            bot.send_message(callback_data.from_user.id, answers.NOORDERS,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.edit_message_reply_markup(callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=markups.EMPTYINL)
        bot.send_message(callback_data.from_user.id, answers.ORDERGETID)
        bot.set_state(callback_data.from_user.id, states.delord, callback_data.message.chat.id)

    def getdelordid(self, message : Message, bot : TeleBot, users, answers, markups):
        """This function gets id of deleting order and deletes it"""

        try:
            users.delorder(int(message.text))
        except ValueError:
            bot.send_message(message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.send_message(message.chat.id, answers.ORDERDELSUCCESS,
                        reply_markup=markups.EMPTYINL, parse_mode="Markdown")
        bot.delete_state(message.from_user.id, message.chat.id)

        msg_orders(message, bot, users, answers, markups)

    def badorder(self, message : Message, bot : TeleBot, users, answers, markups):
        """If user haven't this order"""

        bot.send_message(message.chat.id, answers.BADORDER, parse_mode="Markdown")
        bot.delete_state(message.from_user.id, message.chat.id)

        msg_orders(message, bot, users, answers, markups)

    def courierorderror(self, message : Message, bot : TeleBot, users, answers, markups):
        """Error: order has courier"""

        bot.send_message(message.chat.id, answers.COURIERORDERROR,
                        reply_markup=markups.EMPTYINL, parse_mode="Markdown")
        bot.delete_state(message.from_user.id, message.chat.id)

        msg_orders(message, bot, users, answers, markups)
