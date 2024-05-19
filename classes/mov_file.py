from classes.file import File
from datetime import datetime, timedelta
import ffmpeg

class MovFile(File):
	def get_datetime(self):
		vid = ffmpeg.probe(self.get_path())
		try:
			date_string = vid["streams"][0]["tags"]["creation_time"]
			dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.000000Z")
			# Return None if the datetime is the Unix epoch time
			if dt <= datetime(1970, 1, 1):
				return None
			return dt - timedelta(hours=4)
		except (IndexError, KeyError):
			return None
