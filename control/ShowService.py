# control/ShowService.py
from dao.PhotoDAO import PhotoDAO
from entity.Personal import Personal
from entity.Community import Community

class ShowService:

    def __init__(self):
        self.dao = PhotoDAO()

    def getMyPhotos(self, userid) -> Personal:
        raw_photos = self.dao.findByUser(userid)
        return Personal(personalId=userid, userId=userid, photoList=raw_photos)

    def getPublicPhotos(self) -> Community:
        raw_public_photos = self.dao.findPublic()
        return Community(communityId=1, publicPhotos=raw_public_photos)

    def publishPhoto(self, pid) -> bool:
        try:
            self.dao.setPublic(pid)
            return True
        except Exception as e:
            print(f"Publish error: {e}")
            return False

    def unpublishPhoto(self, pid) -> bool:
        try:
            self.dao.setPrivate(pid)
            return True
        except Exception as e:
            print(f"Unpublish error: {e}")
            return False