"""
This file will register functions as handlers
"""

from telebot import TeleBot

from bot.answers import Buttons, Callbacks

from bot.handlers.registercheck import checkreg
from bot.handlers.reghandlers import Register
from bot.handlers.texthandler import bad_request
from bot.handlers.profilehandlers import Profile
from bot.handlers.careerhandlers import Career
from bot.handlers.orderhandlers import Orders
from bot.handlers.cancelaction import cancel_action
from bot.handlers.databasecommands import getusersdb, delusrdb, delorddb


register = Register()
profile = Profile()
career = Career()
orders = Orders()


def register_handlers(bot : TeleBot, users, helpers, states):
    """This function register all handlers in necessary order"""

    # Db for admins
    register_db_handlers(bot, helpers)

    # Register
    register_reg_handlers(bot, helpers, states)

    # Checking registration
    bot.register_message_handler(callback=checkreg,
                                 func=lambda msg: not users.checkuser(msg.chat.id),
                                 pass_bot=True)

    # Cancel action
    bot.register_message_handler(callback=cancel_action,
                                 state='*',
                                 func=lambda msg: msg.text.lower() == "отмена",
                                 pass_bot=True)

    # Profile
    register_profile_handlers(bot, helpers, states)

    # Courier
    register_courier_handlers(bot, helpers, states, users)

    # Orders
    register_orders_handlers(bot, helpers, states, users)

    bot.register_message_handler(callback=bad_request, pass_bot=True)

def register_db_handlers(bot : TeleBot, helpers):
    """Registers db commands"""

    bot.register_message_handler(callback=getusersdb,
                                 commands=['getusers'],
                                 func=lambda msg: helpers.checkpremission(int(msg.chat.id)),
                                 pass_bot=True)
    bot.register_message_handler(callback=delusrdb,
                                 commands=['delusr'],
                                 func=lambda msg: helpers.checkpremission(int(msg.chat.id)),
                                 pass_bot=True)
    bot.register_message_handler(callback=delorddb,
                                 commands=['delord'],
                                 func=lambda msg: helpers.checkpremission(int(msg.chat.id)),
                                 pass_bot=True)

def register_reg_handlers(bot : TeleBot, helpers, states):
    """Registers registration handlers"""

    bot.register_message_handler(callback=register.start, commands=["start"], pass_bot=True)
    bot.register_message_handler(callback=register.getnumber,
                                 state=states.regnumber,
                                 func=lambda msg: helpers.checknum(msg.text),
                                 pass_bot=True)
    bot.register_message_handler(callback=register.errorgetnumber,
                                 state=states.regnumber,
                                 pass_bot=True)
    bot.register_message_handler(callback=register.getroom,
                                 state=states.regroom,
                                 func=lambda msg: helpers.checkroom(msg.text),
                                 pass_bot=True)
    bot.register_message_handler(callback=register.errorgetroom,
                                 state=states.regroom,
                                 pass_bot=True)

def register_profile_handlers(bot : TeleBot, helpers, states):
    """Registers profile handlers"""

    bot.register_callback_query_handler(callback=profile.changenumber,
                                        func=lambda c: c.data == Callbacks.CALLBACKNUMBER,
                                        pass_bot=True)
    bot.register_callback_query_handler(callback=profile.changeroom,
                                        func=lambda c: c.data == Callbacks.CALLBACKROOM,
                                        pass_bot=True)


    bot.register_message_handler(callback=profile.myprofile,
                                 regexp=Buttons.PROFILEBTN, pass_bot=True)
    bot.register_message_handler(callback=profile.enterroom,
                                 state=states.updroom,
                                 func=lambda msg: helpers.checkroom(msg.text),
                                 pass_bot=True)
    bot.register_message_handler(callback=profile.errorupdroom,
                                 state=states.updroom,
                                 pass_bot=True)
    bot.register_message_handler(callback=profile.enternumber,
                                 state=states.updnumber,
                                 func=lambda msg: helpers.checknum(msg.text),
                                 pass_bot=True)
    bot.register_message_handler(callback=profile.errorupdnumber,
                                 state=states.updnumber,
                                 pass_bot=True)

def register_courier_handlers(bot : TeleBot, helpers, states, users):
    """Registers courier handlers"""

    bot.register_callback_query_handler(callback=career.regcourier,
                                        func=lambda c: c.data == Callbacks.CALLBACKCOURIERREG,
                                        pass_bot=True)
    bot.register_callback_query_handler(callback=career.editcourierstatus,
                                        func=lambda c: c.data == Callbacks.CALLBACKCOURIERCHST,
                                        pass_bot=True)
    bot.register_callback_query_handler(callback=career.getcourierprice,
                                        func=lambda c: c.data == Callbacks.CALLBACKCOURIERPRICE,
                                        pass_bot=True)
    bot.register_callback_query_handler(callback=career.orderscouriermain,
                                        func=lambda c: c.data == Callbacks.CALLBACKCOURIERMYORD,
                                        pass_bot=True)
    bot.register_callback_query_handler(callback=career.takeorder,
                                        func=lambda c: c.data.startswith\
                                            (Callbacks.CALLBACKTAKEORDER),
                                        pass_bot=True)
    bot.register_callback_query_handler(callback=career.didordercourier,
                                        func=lambda c: c.data == Callbacks.CALLBACKCOURIERDIDORD,
                                        pass_bot=True)
    bot.register_callback_query_handler(callback=career.allorders, \
                                        func=lambda c: c.data == Callbacks.CALLBACKAORDERS,
                                        pass_bot=True)


    bot.register_message_handler(callback=career.couriermain,
                                 regexp=Buttons.COURIERBTN, pass_bot=True)
    bot.register_message_handler(callback=career.editprice,
                                 state=states.courierprice,
                                 func=lambda msg: msg.text.isdigit() and \
                                    helpers.checkprice(int(msg.text)),
                                 pass_bot=True)
    bot.register_message_handler(callback=career.errorprice,
                                 state=states.courierprice,
                                 pass_bot=True)
    bot.register_message_handler(callback=career.badcourierorder,
                                 state=states.courierdelord,
                                 func=lambda msg: not msg.text.isdigit() or not \
                                    users.checkorderid(int(msg.text)) or not \
                                    users.getorder(int(msg.text))[3] == msg.chat.id,
                                 pass_bot=True)
    bot.register_message_handler(callback=career.getiddidord,
                                 state=states.courierdelord,
                                 pass_bot=True)

def register_orders_handlers(bot : TeleBot, helpers, states, users):
    """Registers orders handlers"""

    bot.register_callback_query_handler(callback=orders.createorder,
                                        func=lambda c: c.data == Callbacks.CALLBACKNEWORDER,
                                        pass_bot=True)
    bot.register_callback_query_handler(callback=orders.delorder,
                                        func=lambda c: c.data == Callbacks.CALLBACKDELORDER,
                                        pass_bot=True)


    bot.register_message_handler(callback=orders.ordersmain, regexp=Buttons.ORDERSBTN, \
                                 pass_bot=True)
    bot.register_message_handler(callback=orders.getordprice,
                                 state=states.getordprice,
                                 func=lambda msg: msg.text.isdigit() and \
                                    helpers.checkprice(int(msg.text)),
                                 pass_bot=True)
    bot.register_message_handler(callback=orders.incorrectordprice,
                                 state=states.getordprice,
                                 pass_bot=True)
    bot.register_message_handler(callback=orders.incorrectcomment,
                                 state=states.getordcomm,
                                 func=lambda msg: not helpers.checkcomment(msg.text),
                                 pass_bot=True)
    bot.register_message_handler(callback=orders.regorder,
                                 state=states.getordcomm,
                                 pass_bot=True)
    bot.register_message_handler(callback=orders.badorder,
                                 state=states.delord,
                                 func=lambda msg: not msg.text.isdigit() or not \
                                    users.checkorderid(int(msg.text)) or not \
                                    users.checkuserorder(int(msg.text), msg.chat.id),
                                 pass_bot=True)
    bot.register_message_handler(callback=orders.courierorderror,
                                 state=states.delord,
                                 func=lambda msg: msg.text.isdigit() and \
                                    users.checkordercourier(int(msg.text)),
                                 pass_bot=True)
    bot.register_message_handler(callback=orders.getdelordid,
                                 state=states.delord,
                                 pass_bot=True)
