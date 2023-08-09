"""
File with class that helps to work with sqlite
"""

from sqlite3 import connect as sqconnect
import os


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
        """This function checks does param with some paramname is exists"""

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

    def adduser(self, params : list) -> None:
        """This function add given user to current table"""

        userid = params[0]

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

    def edituser(self, editname : str, editval, userid : int) -> None:
        """This function edit user param by user id"""

        if not self.checkuser(userid):
            raise ValueError("This data is not exists")
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE users set {editname}=? where id=?""", \
                        (editval, userid))
            con.commit()

    def getuser(self, userid : int) -> None:
        """This function gets one user with given id"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute("""SELECT * FROM users WHERE id=?""", \
                               (userid, ))
            return info.fetchone()
        return None
