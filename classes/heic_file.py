from classes.file import File
from datetime import datetime
from PIL import Image


class HeicFile(File):
	def get_datetime(self):
		image = Image.open(self.get_path())
		date_string = image.getexif()[306]
		return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
