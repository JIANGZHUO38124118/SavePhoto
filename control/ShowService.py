# control/ShowService.py
from dao.PhotoDAO import PhotoDAO
 
class ShowService:
 
    def __init__(self):
        self.dao = PhotoDAO()
 
    def getMyPhotos(self, userid):
        return self.dao.findByUser(userid)
 
    def getPublicPhotos(self):
        return self.dao.findPublic()
 
    def setPublic(self, pid):
        self.dao.setPublic(pid)

    def setPrivate(self, pid):
        self.dao.setPrivate(pid)