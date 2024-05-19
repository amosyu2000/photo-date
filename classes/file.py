import os


class File:
	def __init__(self, path):
		self.path = path
		self.path_head, self.path_tail = os.path.split(self.get_path())
		self.name, extension = os.path.splitext(self.get_path_tail())
		self.extension = extension.lower()

	def __repr__(self):
		return self.get_path()

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
		raise NotImplementedError(f"Method not implemented for file '{self.get_path()}'")

	def rename(self, new_name, suffix=0):
		try:
			new_suffixed_name = f"{new_name}_{suffix}" if suffix > 0 else new_name
			new_path_tail = f"{new_suffixed_name}{self.get_extension()}"

			if (self.get_path_tail() == new_path_tail):
				return None

			os.rename(self.get_path(), f"{self.get_path_head()}/{new_path_tail}")
			return new_path_tail
		except FileExistsError:
			return self.rename(new_name, suffix + 1)
