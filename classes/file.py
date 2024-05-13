from datetime import datetime, timedelta
from PIL import Image
import ffmpeg
import os

class File:
	def __init__(self, path):
		self.path = path
		self.path_head, self.path_tail = os.path.split(self.get_path())
		self.name, extension = os.path.splitext(self.get_path_tail())
		self.extension = extension.lower()

	def __repr__(self):
		return self.full_path

	def get_path(self):
		return self.path

	def get_path_head(self):
		return self.path_head

	def get_path_tail(self):
		return self.path_tail

	def get_name(self):
		return self.name

	def get_extension(self):
		return self.extension

	def get_datetime(self):
		"""
		Return the date and time information about a photo/video as a datetime object.
		"""
		extension = self.get_extension()
		if (extension == ".heic"):
			image = Image.open(self.get_path())
			return datetime.strptime(image.getexif()[306], "%Y:%m:%d %H:%M:%S")
		elif (extension == ".mov" or extension == ".mp4"):
			vid = ffmpeg.probe(self.get_path())
			try:
				date_string = vid['streams'][0]['tags']['creation_time']
				dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.000000Z")
				# Return None if the datetime is the Unix epoch time
				if (dt <= datetime(1970, 1, 1)):
					return None
				return dt - timedelta(hours=4)
			except (IndexError, KeyError):
				return None
		else:
			image = Image.open(self.get_path())
			exif = image._getexif()
			if (exif):
				date_string = exif.get(36867)
				if (date_string is not None):
					return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")

	def rename(self, new_name, suffix=0):
		try:
			new_suffixed_name = f"{new_name}_{suffix}" if suffix > 0 else new_name
			print(f"{self.get_path_tail()}\t->\t{new_suffixed_name}")
			os.rename(self.get_path(), f"{self.get_path_head()}/{new_suffixed_name}{self.get_extension()}")
		except (FileExistsError):
			self.rename(new_name, suffix+1)
