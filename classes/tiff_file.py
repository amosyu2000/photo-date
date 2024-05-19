from classes.file import File
from datetime import datetime
from PIL import Image


class TiffFile(File):
	def get_datetime(self):
		image = Image.open(self.get_path())
		date_string = image.tag[36867][0]
		image.close()
		return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
