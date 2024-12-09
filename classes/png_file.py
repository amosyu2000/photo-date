from classes.file import File
from datetime import datetime
from PIL import Image


class PngFile(File):
    CREATION_TIME_EXIF_KEY = 'Creation Time'

    def get_datetime(self):
        image = Image.open(self.get_path())
        image.load()
        exif = image.info
        image.close()
        if self.CREATION_TIME_EXIF_KEY in exif:
            date_string = exif[self.CREATION_TIME_EXIF_KEY]
            if date_string is None or date_string == "0000:00:00 00:00:00":
                return None
            return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
