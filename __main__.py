from classes.csv_logger import CsvLogger
from classes.file_factory import FileFactory
from classes.incremental_name_generator import IncrementalNameGenerator
from pillow_heif import register_heif_opener
import glob
import os


class Main:
	# CONSTANTS
	PHOTO_DIRECTORY = "D:/Photos"

	def __init__(self):
		# Add .heic file support to pillow
		register_heif_opener()

		# Get all files in given directory
		files = [FileFactory(path).get_file() for path in glob.glob(f"{self.get_directory()}/**/*", recursive=True) if not os.path.isdir(path)]

		# Confirm that the user wants to rename the files
		confirmation = input(f"Rename {len(files)} files in directory '{os.path.basename(self.get_directory())}'? This action cannot be undone. (Y/n) ")
		if (confirmation != "Y"):
			return

		files.sort(key=lambda file: file.get_path(), reverse=True)
		logger = CsvLogger()
		name_generator = IncrementalNameGenerator(len(files))

		while len(files) > 0:
			# Gather files with the same name into a list
			like_files = [files.pop()]
			while len(files) > 0 and files[-1].get_name() == like_files[0].get_name():
				like_files.append(files.pop())

			# Search for a non-zero datetime from the list of like files
			dt = None
			for file in like_files:
				file_dt = None
				try:
					file_dt = file.get_datetime()
				except NotImplementedError as e:
					print(e)
				if file_dt is not None:
					dt = file_dt
					break

			# Apply the same datetime name to all like files
			new_name = self.get_datetime_name(dt) if dt is not None else name_generator.generate_name()
			for file in like_files:
				logger.log((file.get_path_tail(), file.rename(new_name)))

		logger.save(os.path.dirname(self.get_directory()))

	def get_datetime_name(self, dt):
		"""
		Return the new name for a file given its datetime information.
		"""
		return f"{dt.year}_{dt.month:02d}_{dt.day:02d}-{dt.hour:02d}_{dt.minute:02d}_{dt.second:02d}"

	def get_directory(self):
		return self.PHOTO_DIRECTORY


if __name__ == "__main__":
	Main()
