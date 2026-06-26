from dao.PhotoDAO import PhotoDAO


class DeleteService:

    def __init__(self):

        self.dao = PhotoDAO()

    def delete(self,pid):

        self.dao.deletePhoto(pid)