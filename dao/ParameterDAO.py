# dao/ParameterDAO.py
import sqlite3
from entity.Parameter import Parameter
 
class ParameterDAO:
 
    def get_conn(self):
        return sqlite3.connect("database/photo.db")
 
    def insertParameter(self, parameter):
        conn = self.get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO parameter(photoid, name, value) VALUES (?, ?, ?)',
                (parameter.photoid, parameter.name, parameter.value)
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()
 
    def findByPhoto(self, photo_id):
        conn = self.get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name, value FROM parameter WHERE photoid = ?", (photo_id,))
            rows = cursor.fetchall()
            parameters = []
            for row in rows:
                parameters.append(Parameter(key=row[0], value=row[1]))
            return parameters
        finally:
            cursor.close()
            conn.close()
 
    def deleteByPhoto(self, photoid):
        conn = self.get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM parameter WHERE photoid = ?', (photoid,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
 
    def save(self, photo_id, parameter):
        conn = self.get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO parameter (photoid, name, value) VALUES (?, ?, ?)", 
                (photo_id, parameter.key, parameter.value)
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()