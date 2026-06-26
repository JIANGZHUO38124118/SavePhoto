import sqlite3
from entity.Photo import Photo
from dao.ParameterDAO import ParameterDAO


class PhotoDAO:

    def __init__(self):
        self.conn = sqlite3.connect("database/photo.db")
        self.parameterDao = ParameterDAO()

    def insertPhoto(self, photo):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO photo
            (filename, filepath, visibility, owner)
            VALUES (?, ?, ?, ?)
        """, (
            photo.filename,
            photo.filepath,
            photo.visibility,
            photo.owner
        ))

        self.conn.commit()

        return cursor.lastrowid

    def findByUser(self, userid):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT photoid, filename, filepath, visibility, owner
            FROM photo
            WHERE owner=?
        """, (userid,))

        rows = cursor.fetchall()

        photos = []

        for row in rows:
            parameters = self.parameterDao.findByPhoto(row[0])

            photo = Photo(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                parameters
            )

            photos.append(photo)

        return photos

    def findPublic(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT photoid, filename, filepath, visibility, owner
            FROM photo
            WHERE visibility=1
        """)

        rows = cursor.fetchall()

        photos = []

        for row in rows:
            parameters = self.parameterDao.findByPhoto(row[0])

            photo = Photo(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                parameters
            )

            photos.append(photo)

        return photos

    def deletePhoto(self, pid):

        cursor = self.conn.cursor()

        cursor.execute("""
            DELETE FROM photo
            WHERE photoid=?
        """, (pid,))

        self.conn.commit()

    def setPublic(self, pid):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE photo
            SET visibility=1
            WHERE photoid=?
        """, (pid,))

        self.conn.commit()