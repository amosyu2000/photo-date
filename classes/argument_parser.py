import argparse


class ArgumentParser:
	PROG = "Photo Date"
	DESCRIPTION = "Rename photos based on their date metadata."
	HELP_DIRECTORY = "The target directory."

	def __init__(self):
		self.parser = argparse.ArgumentParser(prog=self.PROG, description=self.DESCRIPTION)
		self.parser.add_argument('-d', '--directory', required=True, help=self.HELP_DIRECTORY)

	def get_parser(self):
		return self.parser

	def get_directory_arg(self):
		return self.parse_args().directory

	def parse_args(self):
		return self.get_parser().parse_args()
