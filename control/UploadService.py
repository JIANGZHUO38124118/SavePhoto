import shutil
import os

from dao.PhotoDAO import PhotoDAO
from entity.Photo import Photo


class UploadService:

    def __init__(self):

        self.dao = PhotoDAO()

    def upload(self,path,userid):

        filename = os.path.basename(path)

        target = f"photos/uploads/{filename}"

        shutil.copy(path,target)

        photo = Photo(
            None,
            filename,
            target,
            0,
            userid
        )

        self.dao.insertPhoto(photo)