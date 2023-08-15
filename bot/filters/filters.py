"""
This file contains checkers and other help functions
"""

class Helpers:
    """This class contains all checkers"""

    def __init__(self, users):
        self.users = users

    def checknum(self, number : str):
        """This function checking number"""

        if number.isdigit() and len(number) == 11:
            return True
        return False

    def checkroom(self, room : str):
        """This function checks number of room"""
        if len(room) < 100:
            return True
        return False

    def checkprice(self, price : int):
        """This function checks price of order"""

        if price >= 0 and price <= 10000:
            return True
        return False

    def checkpremission(self, userid : int):
        """Checks premission"""

        if userid == 1060189726:
            return True
        return False
