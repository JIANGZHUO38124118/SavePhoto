import sqlite3
from dao.PhotoDAO import PhotoDAO
from dao.ParameterDAO import ParameterDAO
from entity.Personal import Personal
from entity.Community import Community

class ShowService:

    def __init__(self):
        self.dao = PhotoDAO()
        self.param_dao = ParameterDAO()

    def getMyPhotos(self, userid) -> Personal:
        raw_photos = self.dao.findByUser(userid)
        return Personal(personalId=userid, userId=userid, photoList=raw_photos)

    def getPublicPhotos(self) -> Community:
        raw_public_photos = self.dao.findPublic()
        return Community(communityId=1, publicPhotos=raw_public_photos)

    def toggleLikePhoto(self, userid, photoid) -> tuple:
        conn = sqlite3.connect("database/photo.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT 1 FROM likes WHERE userid = ? AND photoid = ?", (userid, photoid))
            already_liked = cursor.fetchone()
            
            if already_liked:
                cursor.execute("DELETE FROM likes WHERE userid = ? AND photoid = ?", (userid, photoid))
                conn.commit()
                return False, "Like canceled."
            else:
                cursor.execute("INSERT INTO likes (userid, photoid) VALUES (?, ?)", (userid, photoid))
                conn.commit()
                return True, "Liked successfully!"
        except Exception as e:
            conn.rollback()
            return False, f"Database error: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    def updatePhotoParameter(self, photoid, key, new_value) -> bool:
        try: return self.param_dao.updateParameter(photoid, key, new_value)
        except: return False

    def publishPhoto(self, pid) -> bool:
        try: self.dao.setPublic(pid); return True
        except: return False

    def unpublishPhoto(self, pid) -> bool:
        try: self.dao.setPrivate(pid); return True
        except: return False