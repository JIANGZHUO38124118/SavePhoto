class Photo:

    def __init__(
            self,
            photoid,
            filename,
            filepath,
            visibility,
            owner,
            parameter):

        self.photoid = photoid
        self.filename = filename
        self.filepath = filepath
        self.visibility = visibility
        self.owner = owner
        self.parameter = parameter