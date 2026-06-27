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

    def findByPhoto(self, photo_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name, value FROM parameter WHERE photoid = ?
        """, (photo_id,))
        
        rows = cursor.fetchall()
        parameters = []
        for row in rows:
            parameters.append(Parameter(key=row[0], value=row[1]))
            
        return parameters

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

    def save(self, photo_id, parameter):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO parameter (photoid, name, value) 
            VALUES (?, ?, ?)
        """, (
            photo_id, 
            parameter.key,
            parameter.value
        ))
        self.conn.commit()