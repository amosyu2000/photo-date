from pillow_heif import register_heif_opener
from classes.file import File
import glob
import uuid

# CONSTANTS
PHOTO_DIRECTORY = "C:/Users/Dell/Downloads/2023"

def get_datetime_name(dt):
	"""
	Return the new name for a file given its datetime information.
	"""
	return f"{dt.year}_{dt.month:02d}_{dt.day:02d}-{dt.hour:02d}_{dt.minute:02d}_{dt.second:02d}"

def get_random_name():
	return f"misc_{str(uuid.uuid4())[:8]}"

if __name__ == '__main__':
	# Add .heic file support to pillow
	register_heif_opener()

	# Get all files in given directory
	files = [ File(path) for path in glob.glob(f"{PHOTO_DIRECTORY}/*") ]
	files.sort(key=lambda file: file.get_path(), reverse=True)

	while len(files) > 0:
		# Gather files with the same name into a list
		like_files = [ files.pop() ] 
		while(len(files) > 0 and files[-1].get_name() == like_files[0].get_name()):
			like_files.append(files.pop())

		# Search for a non-zero datetime from the list of like paths
		dt = None
		for file in like_files:
			file_dt = file.get_datetime()
			if (file_dt is not None):
				dt = file_dt
				break

		# Apply the same datetime name to all like paths
		new_name = get_datetime_name(dt) if dt is not None else get_random_name()
		for file in like_files:
			if (new_name != file.get_name()):
				file.rename(new_name)
