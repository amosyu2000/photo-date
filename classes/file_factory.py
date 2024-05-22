from classes.file import File
from classes.heic_file import HeicFile
from classes.jpg_file import JpgFile
from classes.mov_file import MovFile
from classes.tiff_file import TiffFile


class FileFactory:
    def __init__(self, path):
        file = File(path)
        extension = file.get_extension()
        if extension in [".heic"]:
            self.file = HeicFile(file.get_path())
        elif extension in [".jpg", ".jpeg", ".png", ".jfif", ".cr2", ".webp"]:
            self.file = JpgFile(file.get_path())
        elif extension in [".mov", ".mp4", ".avi"]:
            self.file = MovFile(file.get_path())
        elif extension in [".nef"]:
            self.file = TiffFile(file.get_path())
        else:
            self.file = file

    def get_file(self):
        return self.file
