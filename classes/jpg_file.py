from classes.file import File
from datetime import datetime
from PIL import Image
import piexif


class JpgFile(File):
    def get_datetime(self):
        image = Image.open(self.get_path())
        exif = image._getexif()
        image.close()
        if exif:
            date_string = exif.get(36867)
            if date_string is None or date_string == "0000:00:00 00:00:00":
                return None
            return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")

    def set_datetime(self, new_dt):
        exif_dict = piexif.load(self.get_path())
        date_string = new_dt.strftime('%Y:%m:%d %H:%M:%S')
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_string
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date_string
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, self.get_path())
