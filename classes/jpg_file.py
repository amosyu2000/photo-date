from classes.file import File
from datetime import datetime
from PIL import Image


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
