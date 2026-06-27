# entity/Personal.py
from entity.Photo import Photo

class Personal:

    def __init__(self, personalId: int, userId: int, photoList=None):
        self.personalId = personalId
        self.userId = userId
        self.photoList = photoList if photoList is not None else []

    def addPhoto(self, photo: Photo) -> None:
        self.photoList.append(photo)

    def removePhoto(self, photoId: int) -> None:
        self.photoList = [p for p in self.photoList if p.photoid != photoId]

    def getPhotos(self) -> list:
        return self.photoList