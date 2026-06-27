# dao/PhotoDAO.py
import sqlite3
from entity.PhotoVisibility import PhotoVisibility
from entity.Photo import Photo
from dao.ParameterDAO import ParameterDAO

class PhotoDAO:

    def __init__(self):
        self.conn = sqlite3.connect("database/photo.db")
        self.parameterDao = ParameterDAO()

    def insertPhoto(self, photo):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO photo (filename, filepath, visibility, owner)
                VALUES (?, ?, ?, ?)
            """, (
                photo.filename,
                photo.filepath,
                photo.visibility.value,
                photo.owner
            ))
            self.conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def findByUser(self, userid):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT p.photoid, p.filename, p.filepath, p.visibility, p.owner,
                       (SELECT COUNT(*) FROM likes l WHERE l.photoid = p.photoid) AS likes_count
                FROM photo p 
                WHERE p.owner=?
            """, (userid,))
            rows = cursor.fetchall()

            photos = []
            for row in rows:
                parameters = self.parameterDao.findByPhoto(row[0])
                photo = Photo(row[0], row[1], row[2], row[3], row[4], parameters)
                photo.likes_count = row[5] 
                photos.append(photo)
            return photos
        finally:
            cursor.close()

    def findPublic(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT p.photoid, p.filename, p.filepath, p.visibility, p.owner, u.account,
                       (SELECT COUNT(*) FROM likes l WHERE l.photoid = p.photoid) AS likes_count
                FROM photo p
                LEFT JOIN user u ON p.owner = u.userid
                WHERE p.visibility = ?
            """, (PhotoVisibility.PUBLIC.value,))
            rows = cursor.fetchall()

            photos = []
            for row in rows:
                parameters = self.parameterDao.findByPhoto(row[0])
                photo = Photo(row[0], row[1], row[2], row[3], row[4], parameters)
                
                photo.owner_account = row[5] if row[5] else "Unknown"
                photo.likes_count = row[6]
                
                photos.append(photo)
            return photos
        finally:
            cursor.close()

    def deletePhoto(self, pid):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM photo WHERE photoid=?", (pid,))
            self.conn.commit()
        finally:
            cursor.close()

    def setPublic(self, pid):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE photo SET visibility = ? WHERE photoid = ?", (PhotoVisibility.PUBLIC.value, pid))
            self.conn.commit()
        finally:
            cursor.close()

    def setPrivate(self, pid):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE photo SET visibility = ? WHERE photoid = ?", (PhotoVisibility.PRIVATE.value, pid))
            self.conn.commit()
        finally:
            cursor.close()