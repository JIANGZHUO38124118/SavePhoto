# entity/Community.py
class Community:

    def __init__(self, communityId: int, publicPhotos=None):
        self.communityId = communityId
        self.publicPhotos = publicPhotos if publicPhotos is not None else []

    def getPublicPhotos(self) -> list:
        return self.publicPhotos