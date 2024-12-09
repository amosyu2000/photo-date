from classes.jpg_file import JpgFile
from datetime import datetime
from PIL import Image
from pillow_heif import register_heif_opener


class HeicFile(JpgFile):
    def __init__(self, path):
        register_heif_opener()
        super().__init__(path)

    def get_datetime(self):
        image = Image.open(self.get_path())
        date_string = image.getexif()[306]
        image.close()
        return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
