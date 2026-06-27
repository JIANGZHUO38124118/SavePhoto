
class Photo:

    def __init__(self, photoid, filename, filepath, visibility, owner, parameter=None):
        from entity.PhotoVisibility import PhotoVisibility
        
        self.photoid = photoid
        self.filename = filename
        self.filepath = filepath
        
        if isinstance(visibility, PhotoVisibility):
            self.visibility = visibility
        else:
            self.visibility = PhotoVisibility(visibility)
            
        self.owner = owner
        self.parameter = parameter if parameter is not None else []

    def isPublic(self) -> bool:
        from entity.PhotoVisibility import PhotoVisibility
        return self.visibility == PhotoVisibility.PUBLIC

    def getPhotoId(self) -> int:
        return self.photoid

    def getFilePath(self) -> str:
        return self.filepath
        
    def getVisibility(self):
        return self.visibility