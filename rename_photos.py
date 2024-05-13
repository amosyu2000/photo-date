from datetime import datetime, timedelta
from PIL import Image
from pillow_heif import register_heif_opener
import glob
import os
import pytz
import uuid
import ffmpeg

# CONSTANTS
PHOTO_DIRECTORY = "C:/Users/Dell/Downloads/2000-10-20 Baby Photos"

class FilePath:
	def __init__(self, full_path):
		self.full_path = full_path
		self.head, self.tail = os.path.split(self.full_path)
		self.file_name, file_extension = os.path.splitext(self.tail)
		self.file_extension = file_extension.lower()
	def __repr__(self):
		return self.full_path

def get_datetime(path:FilePath):
	"""
	Return the date and time information about a photo/video as a datetime object.
	"""

	extension = path.file_extension

	if (extension == ".heic"):
		image = Image.open(path.full_path)
		return datetime.strptime(image.getexif()[306], "%Y:%m:%d %H:%M:%S")
	elif (extension == ".mov" or extension == ".mp4"):
		vid = ffmpeg.probe(path.full_path)
		try:
			date_string = vid['streams'][0]['tags']['creation_time']
			dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.000000Z")
			# Return None if the datetime is the Unix epoch time
			if (dt <= datetime(1970, 1, 1)):
				return None
			return dt - timedelta(hours=4)
		except (IndexError, KeyError):
			print(vid['streams'][0]['tags'])
			return None
	else:
		image = Image.open(path.full_path)
		exif = image._getexif()
		if (exif):
			date_string = exif.get(36867)
			if (date_string != None):
				return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")

def get_datetime_name(dt:datetime):
	"""
	Return the new name for a file given its datetime information.
	"""
	return f"{dt.year}_{dt.month:02d}_{dt.day:02d}-{dt.hour:02d}_{dt.minute:02d}_{dt.second:02d}"

def get_random_name():
	return f"misc_{str(uuid.uuid4())[:8]}"

def rename(path, new_name, suffix=0):
	try:
		new_suffixed_name = f"{new_name}_{suffix}" if suffix > 0 else new_name
		print(f"{path.tail}\t->\t{new_suffixed_name}")
		os.rename(path.full_path, f"{path.head}/{new_suffixed_name}{path.file_extension}")
	except (FileExistsError):
		rename(path, new_name, suffix+1)

if __name__ == '__main__':
	# Add .heic file support to pillow
	register_heif_opener()

	# Get all files in given directory
	paths = [ FilePath(path) for path in glob.glob(f"{PHOTO_DIRECTORY}/*") ]
	paths.sort(key=lambda path: path.full_path, reverse=True)

	while len(paths) > 0:
		# Gather files with the same name into a list
		like_paths = [ paths.pop() ] 
		while(len(paths) > 0 and paths[-1].file_name == like_paths[0].file_name):
			like_paths.append(paths.pop())

		# Search for a non-zero datetime from the list of like paths
		dt = None
		for path in like_paths:
			path_dt = get_datetime(path)
			if (path_dt != None):
				dt = path_dt
				break

		# Apply the same datetime name to all like paths
		new_name = get_datetime_name(dt) if dt != None else get_random_name()
		for path in like_paths:
			if (new_name != path.file_name):
				rename(path, new_name)