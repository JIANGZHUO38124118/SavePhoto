# control/UploadService.py
from dao.PhotoDAO import PhotoDAO
from dao.ParameterDAO import ParameterDAO

class UploadService:

    def __init__(self):
        self.photoDAO = PhotoDAO()
        self.parameterDAO = ParameterDAO()

    def uploadPhoto(self, photo, parameter_list=None) -> bool:
        try:
            photo_id = self.photoDAO.insertPhoto(photo)
            if parameter_list and photo_id:
                for param in parameter_list:
                    self.parameterDAO.save(photo_id, param)
                
            return True
        except Exception as e:
            print(f"Upload Service Error: {e}")
            return False