import sqlite3

from entity.User import User


class UserDAO:

    def __init__(self):

        self.conn = sqlite3.connect(
            "database/photo.db"
        )

    def insertUser(self,user):

        cursor = self.conn.cursor()

        cursor.execute(
            '''
            INSERT INTO user
            (
                account,
                password,
                username
            )
            VALUES
            (
                ?,?,?
            )
            ''',
            (
                user.account,
                user.password,
                user.username
            )
        )

        self.conn.commit()

    def findByAccount(self,account):

        cursor = self.conn.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM user
            WHERE account=?
            ''',
            (account,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return User(
            row[0],
            row[1],
            row[2],
            row[3]
        )