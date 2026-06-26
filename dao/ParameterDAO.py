# dao/ParameterDAO.py

import sqlite3
from entity.Parameter import Parameter


class ParameterDAO:

    def __init__(self):
        self.conn = sqlite3.connect("database/photo.db")

    def insertParameter(self, parameter):
        cursor = self.conn.cursor()

        cursor.execute(
            '''
            INSERT INTO parameter(photoid, name, value)
            VALUES (?, ?, ?)
            ''',
            (
                parameter.photoid,
                parameter.name,
                parameter.value
            )
        )

        self.conn.commit()

    def findByPhoto(self, photoid):
        cursor = self.conn.cursor()

        cursor.execute(
            '''
            SELECT parameterid, photoid, name, value
            FROM parameter
            WHERE photoid = ?
            ''',
            (photoid,)
        )

        rows = cursor.fetchall()

        return [
            Parameter(row[0], row[1], row[2], row[3])
            for row in rows
        ]

    def deleteByPhoto(self, photoid):
        cursor = self.conn.cursor()

        cursor.execute(
            '''
            DELETE FROM parameter
            WHERE photoid = ?
            ''',
            (photoid,)
        )

        self.conn.commit()