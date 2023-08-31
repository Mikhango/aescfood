"""
There are states of bot in this file
"""

# Telebot states
from telebot.handler_backends import State, StatesGroup

class States(StatesGroup):
    """
    There are bot's states in this class
    """

    # Reg states
    regnumber = State()
    regroom = State()

    # Profile states
    updnumber = State()
    updroom = State()

    # Order states
    getordroom = State()
    getordprice = State()
    getordcomm = State()
    delord = State()

    # Courier states
    courierprice = State()
    courierdelord = State()
