import math


class IncrementalNameGenerator:
	def __init__(self, total_files:int):
		self.total_files = total_files
		self.index = 0

	def increment_index(self):
		self.set_index(self.get_index() + 1)

	def generate_name(self):
		self.increment_index()
		return f"img{str(self.get_index()).zfill(self.get_total_digits())}"

	def get_index(self):
		return self.index

	def get_total_files(self):
		return self.total_files

	def get_total_digits(self):
		return math.ceil(math.log10(self.get_total_files()))

	def set_index(self, num):
		self.index = num