"""
This file contains checkers and other help functions
"""

class Checkers:
    """This class contains all checkers"""
    def __init__(self):
        pass

    def checknum(self, number : str):
        """This function checking number"""

        if number.isdigit() and len(number) == 11:
            return True
        return False

    def checkroom(self, room : str):
        """This function checks number of room"""

        return True
