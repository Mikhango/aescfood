"""
File with class that helps to work with sqlite
"""

from sqlite3 import connect as sqconnect
import os

from random import randint


class DataBase:
    """
    This class makes work with sqlite easier
    More functions and description in README
    """

    def __init__(self, file : str, namedb : str) -> None:
        self.namedb = self.__getway(file, namedb) + ".db"

    def __getway(self, file : str, namedb : str) -> str:
        return os.path.join(os.path.split(os.path.abspath(file))[0], namedb)

    @property
    def getdbname(self) -> str:
        """This function returns name of current db"""

        return self.namedb

    def checkuser(self, userid : int) -> bool:
        """This function checks is user exists"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM users WHERE id=?""", \
                               (userid, ))
            if info.fetchone() is None:
                return False
        return True

    def createtable(self, nametable : str, params : list) -> None:
        """This function creates table if table is not exists"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            allparams = ''
            for param in params:
                allparams += f"{param[0]} {param[1].upper()}, "
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {nametable}({allparams[:-2]});""")
            con.commit()

    def adduser(self, userid : int, userroom : str, usernum : str) -> None:
        """This function add given user to current table"""

        params = [userid, userroom, usernum]

        if self.checkuser(userid):
            raise ValueError("This data is also exists")
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cnt = len(params)
            cort = tuple(params)
            cur.execute(f"""INSERT INTO users VALUES({("?, " * cnt)[:-2]});""", cort)
            con.commit()

    def deluser(self, userid : int) -> None: # deleting only using param
        """This function delete user with given id"""

        if not self.checkuser(userid):
            raise ValueError("This data is not exists")
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute("""DELETE FROM users WHERE id=?;""", (userid,))
            con.commit()

    def editusernumber(self, userid : int, newnumber : str) -> None:
        """This function edit user number"""

        if not self.checkuser(userid):
            raise ValueError("This data is not exists")
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute("""UPDATE users set number=? where id=?""", \
                        (newnumber, userid))
            con.commit()

    def edituserroom(self, userid : int, newroom : str) -> None:
        """This function edit user room"""

        if not self.checkuser(userid):
            raise ValueError("This data is not exists")
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute("""UPDATE users set room=? where id=?""", \
                        (newroom, userid))
            con.commit()

    def getuser(self, userid : int) -> tuple:
        """This function gets one user with given id"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM users WHERE id=?""", \
                               (userid, ))
            return info.fetchone()

    def checkcourier(self, userid : int) -> bool:
        """This function checks is courier exists"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM couriers WHERE id=?""", \
                               (userid, ))
            if info.fetchone() is None:
                return False
        return True

    def getcourier(self, userid : int) -> tuple:
        """This function gets one user with given id"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM couriers WHERE id=?""", \
                               (userid, ))
            return info.fetchone()

    def getfreecouriers(self):
        """This function gets one user with given id"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM couriers WHERE status=?""", \
                               (1, ))
            return info.fetchall()

    def addcourier(self, userid : int) -> None:
        """This function add given courier to current table"""

        params = [userid, 0, 0, 0]

        if self.checkcourier(userid):
            raise ValueError("This data is also exists")
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cnt = len(params)
            cort = tuple(params)
            cur.execute(f"""INSERT INTO couriers VALUES({("?, " * cnt)[:-2]});""", cort)
            con.commit()

    def changecourierstatus(self, userid : int) -> None:
        """This function edit courier status"""

        if not self.checkuser(userid):
            raise ValueError("This data is not exists")

        newstat = int(not self.getcourier(userid)[1])

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute("""UPDATE couriers set status=? where id=?""", \
                        (newstat, userid))
            con.commit()

    def editcourierprice(self, userid : int, newprice : int) -> None:
        """This function edit courier minimal price"""

        if not self.checkuser(userid):
            raise ValueError("This data is not exists")

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute("""UPDATE couriers set price=? where id=?""", \
                        (newprice, userid))
            con.commit()

    def editcouriermoney(self, userid : int, money : int) -> None:
        """This function edit courier minimal price"""

        if not self.checkcourier(userid):
            raise ValueError("This data is not exists")

        curr = self.getcourier(userid)[3]

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute("""UPDATE couriers set earned=? where id=?""", \
                        (money + curr, userid))
            con.commit()

    def checkorderid(self, idorder : int) -> bool:
        """This function checks if given order id is exists"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM orders WHERE id=?""", \
                               (idorder, ))
            if info.fetchone() is None:
                return False
        return True

    def checkordercourier(self, idorder : int) -> bool:
        """This function checks if given order courier is exists"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM orders WHERE id=?""", \
                               (idorder, ))
            one = info.fetchone()

            if one is None:
                return False
            if one[3] == -1:
                return False

        return True

    def getorder(self, orderid : int) -> tuple:
        """This function gets one order with given id"""

        if not self.checkorderid(orderid):
            raise ValueError("Order is not exists")

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM orders WHERE id=?""", \
                               (orderid, ))
            return info.fetchone()

    def addorder(self, client_id : int, client_name : int, room : str, price : int,
                 comment : str) -> None:
        """This function adds order with need params"""

        id_order = randint(1, 10000)

        while self.checkorderid(id_order):
            id_order = randint(1, 10000)

        params = [id_order, client_id, client_name, -1, "", room, price, comment]

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cnt = len(params)
            cort = tuple(params)
            cur.execute(f"""INSERT INTO orders VALUES({("?, " * cnt)[:-2]});""", cort)
            con.commit()

        return id_order

    def addordercourier(self, orderid : int, courier_id : int, courier_name : str):
        """This functions add courier to order"""

        if not self.checkorderid(orderid):
            raise ValueError("Order is not exists")
        if self.checkordercourier(orderid):
            raise ValueError("Order always has courier")

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute("""UPDATE orders set id_courier=?, name_courier=? where id=?""", \
                        (courier_id, courier_name, orderid))
            con.commit()

    def checkuserorder(self, orderid : int, client_id : int) -> bool:
        """Checks if order is user's"""

        if not self.checkorderid(orderid):
            return False
        return self.getorder(orderid)[1] == client_id

    def delorder(self, orderid : int):
        """This function deletes order from orders table"""

        if not self.checkorderid(orderid):
            raise ValueError("Order is not exists")

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute("""DELETE FROM orders WHERE id=?;""", (orderid,))
            con.commit()

    def getuserorders(self, userid : int) -> list:
        """This function gets all orders of user"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM orders WHERE id_client=?""", \
                               (userid, ))
            allinfo = info.fetchall()
            if allinfo is None:
                return []
            return allinfo

    def getcourierorders(self, userid : int) -> list:
        """This function gets all orders of user"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM orders WHERE id_courier=?""", \
                               (userid, ))
            allinfo = info.fetchall()
            if allinfo is None:
                return []
            return allinfo
