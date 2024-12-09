from classes.confirmation_input import ConfirmationInput
from classes.csv_logger import CsvLogger
from classes.file_factory import FileFactory
from classes.incremental_name_generator import IncrementalNameGenerator
import click
import glob
import os


@click.command()
@click.option('--directory', '-d', required=True, type=click.STRING, help='The directory containing the photos to rename.')
class Rename:
    """Rename photos based on their date metadata. Generates a log after renaming all photos in a given directory."""

    def __init__(self, directory):

        # Get all files in given directory
        files = [FileFactory(path).get_file() for path in glob.glob(f"{directory}/**/*", recursive=True) if not os.path.isdir(path)]

        # Confirm that the user wants to rename the files
        ConfirmationInput(f"Rename {len(files)} files in directory '{os.path.basename(directory)}'?")

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
            new_name = self.get_datetime_name(dt) if dt is not None else name_generator.get_next_name()
            for file in like_files:
                logger.log((file.get_path_tail(), file.rename(new_name)))

        logger.save(os.path.dirname(directory))

    def get_datetime_name(self, dt):
        """
        Return the new name for a file given its datetime information.
        """
        return f"{dt.year}_{dt.month:02d}_{dt.day:02d}-{dt.hour:02d}_{dt.minute:02d}_{dt.second:02d}"
