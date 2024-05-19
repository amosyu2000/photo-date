class CsvLogger:
	FILE_NAME = "photo_date_log"
	FILE_EXTENSION = "csv"

	def __init__(self):
		self.rows = []

	def log(self, tup):
		row = ",".join(f"\"{str(i)}\"" for i in tup)
		self.rows.append(row)

	def get_rows(self):
		return self.rows

	def get_file(self):
		return f"{self.get_file_name()}.{self.get_file_extension()}"

	def get_file_name(self):
		return self.FILE_NAME

	def get_file_extension(self):
		return self.FILE_EXTENSION

	def save(self, dir):
		f = open(f"{dir}/{self.get_file()}", "w")
		f.write("\n".join(self.get_rows()))
		f.close()
		print(f"Generated log file '{self.get_file()}' in directory '{dir}'.")
