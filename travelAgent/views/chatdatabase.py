import sqlite3
from sqlite3 import Error
from datetime import datetime
import time
from os import path

# CONSTANTS

FILE = path.join(path.dirname(__file__), "../messages.db")
PLAYLIST_TABLE = "Messages"
UNSEEN_TABLE = "Unseen"


class DataBase:
    """
    used to connect, write to and read from a local sqlite3 database
    """
    def __init__(self):
        """
        try to connect to file and create cursor
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self):
        """
        close the db connection
        :return: None
        """
        self.conn.close()

    def _create_table(self):
        """
        create new database table if one doesn't exist
        :return: None
        """
        query = f"""CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE}
                    (username TEXT, name TEXT, content TEXT, time Date, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        self.cursor.execute(query)
        self.conn.commit()
        query = f"""CREATE TABLE IF NOT EXISTS {UNSEEN_TABLE}
                    (username TEXT PRIMARY KEY, userunseen INTEGER, adminunseen INTEGER)"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_messages(self, limit=100, username=None):
        # limit=100 代表只想获得数据库里最后100条数据库
        """
        returns all messages
        :param limit: int
        :param username: str
        :return: list[dict]
        """
        if not username:
            query = f"SELECT * FROM {PLAYLIST_TABLE}"
            self.cursor.execute(query)
        else:
            query = f"SELECT * FROM {PLAYLIST_TABLE} WHERE USERNAME = ?"
            self.cursor.execute(query, (username,))

        result = self.cursor.fetchall()

        # return messages in sorted order by date
        results = []
        #通过下面的for获得most reccent message
        for r in sorted(result, key=lambda x: x[4], reverse=True)[:limit]:
            username, name, content, date, _id = r
            # 转换成jason形式
            data = {"username":username, "name":name, "message":content, "time":str(date)}
            results.append(data)

        return list(reversed(results))

    def get_messages_by_username(self, name, limit=100):
        """
        Gets a list of messages by username
        :param name: str
        :return: list
        """
        return self.get_all_messages(limit, name)

    def save_message(self, username, name, msg):
        """
        saves the given message in the table
        :param username: str
        :param name: str
        :param msg: str
        :param time: datetime
        :return: None
        """
        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (username, name, msg, datetime.now(), None))
        # 把message存到table里
        self.conn.commit()

    def get_unseen(self, username, to_user):
        """

        :param username: str
        :param to_user: bool
        :return: int
        """
        if to_user:
            query = f"""SELECT userunseen FROM {UNSEEN_TABLE} WHERE username = ?"""
        else:
            query = f"""SELECT adminunseen FROM {UNSEEN_TABLE} WHERE username = ?"""
        self.cursor.execute(query, (username, ))
        res = self.cursor.fetchone()
        if res is None:
            print('res')
            query = f"""INSERT INTO {UNSEEN_TABLE} VALUES(?, 0, 0)"""
            self.cursor.execute(query, (username, ))
            self.conn.commit()
            return 0
        num = res[0]
        return num

    def set_unseen(self, username, to_user, num):
        """

        :param username: str
        :param to_user: bool
        :param num: int
        :return:
        """
        self.get_unseen(username, to_user)
        if to_user:
            query = f"""UPDATE {UNSEEN_TABLE} SET userunseen = ? WHERE username = ?"""
        else:
            query = f"""UPDATE {UNSEEN_TABLE} SET adminunseen = ? WHERE username = ?"""
        self.cursor.execute(query, (num, username))
        self.conn.commit()

