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
        self.nametable = ""

    def __getway(self, file : str, namedb : str) -> str:
        return os.path.join(os.path.split(os.path.abspath(file))[0], namedb)

    @property
    def getdbname(self) -> str:
        """This function returns name of current db"""

        return self.namedb

    def setnametable(self, nametable : str) -> None:
        """This function sets new name of table"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute(f"""SELECT name FROM sqlite_master WHERE type='table' \
                               AND name='{nametable}'""")
            if info.fetchone() is None:
                raise ValueError(f"Table {nametable} is not exists")
        self.nametable = nametable

    def checkparam(self, paramvalue, paramname : str) -> bool:
        # You need to put paramvalue to func in type it should be
        """This function checks does param with some paramname is exists"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute(f"""SELECT * FROM {self.nametable} WHERE {paramname}=?""", \
                               (paramvalue, ))
            if info.fetchone() is None:
                return False
        return True

    def createtable(self, nametable : str, params : list) -> None:
        """This function creates table if table is not exists"""

        self.nametable = nametable
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            allparams = ''
            for param in params:
                allparams += f"{param[0]} {param[1].upper()}, "
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.nametable}({allparams[:-2]});""")
            con.commit()

    def adddata(self, params : list, paramvalue, paramname : str) -> None:
        """This function add given data to current table"""

        if self.checkparam(paramvalue, paramname):
            raise ValueError("This data is also exists")
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cnt = len(params)
            cort = tuple(params)
            cur.execute(f"""INSERT INTO {self.nametable} VALUES({("?, " * cnt)[:-2]});""", cort)
            con.commit()

    def deldata(self, paramvalue, paramname : str) -> None: # deleting only using param
        """This function delete data with given param from current table"""

        if not self.checkparam(paramvalue, paramname):
            raise ValueError("This data is not exists")
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute(f"""DELETE FROM {self.nametable} WHERE {paramname}=?;""", (paramvalue,))
            con.commit()

    def editdata(self, parbyvalue, parbyname : str, updvalue, updname : str) -> None:
        """This function edit given data with given param in current table"""

        if not self.checkparam(parbyvalue, parbyname):
            raise ValueError("This data is not exists")
        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE {self.nametable} set {updname}=? where {parbyname}=?""", \
                        (updvalue, parbyvalue))
            con.commit()

    def getone(self, parvalue, parname : str) -> tuple:
        """This function gets one row of data with given param"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute(f"""SELECT * FROM {self.nametable} WHERE {parname}=?""", \
                               (parvalue, ))
            return info.fetchone()
        return None

    def getall(self, parvalue, parname : str) -> list:
        """This function gets all rows of data with given param"""

        with sqconnect(self.namedb) as con:
            cur = con.cursor()
            info = cur.execute(f"""SELECT * FROM {self.nametable} WHERE {parname}=?""", \
                                (parvalue, ))
            return info.fetchall()
        return None
