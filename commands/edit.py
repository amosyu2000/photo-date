from classes.confirmation_input import ConfirmationInput
from classes.datetime_unit import DatetimeUnit
from classes.file_factory import FileFactory
from datetime import datetime
import click
import glob
import os


@click.command()
@click.option('--directory', '-d', required=False, type=click.STRING, help='The directory containing the photos to edit.')
@click.option('--files', '-f', 'args_is_files', required=False, is_flag=True, help='The list of photos to edit.')
@click.argument('args', nargs=-1)
class Edit:
    """Edit the Date Taken metadata of photos."""

    def __init__(self, args_is_files, directory, args):

        # Create file objects
        path_args = []
        if (args_is_files):
            path_args = args
        elif (directory):
            path_args = [path for path in glob.glob(f"{directory}/**/*", recursive=True) if not os.path.isdir(path)]
        files = [FileFactory(path).get_file() for path in path_args]
        print(f"Selected {len(files)} files.")

        new_dt = self.get_datetime_input()

        # Confirm that the user wants to edit the files
        ConfirmationInput(f"Set the Date Taken metadata to '{new_dt}' for {len(files)} files?")
        
        for file in files:
            try:
                file.set_datetime(new_dt)
            except NotImplementedError as e:
                print(e)

    def get_datetime_input(self):
        now_dt = datetime.now()
        try:
            return datetime(
                year=self.get_datetime_unit_input(DatetimeUnit(name="year", default_value=now_dt.year)),
                month=self.get_datetime_unit_input(DatetimeUnit(name="month", default_value=now_dt.month, min_value=1, max_value=12)),
                day=self.get_datetime_unit_input(DatetimeUnit(name="day", default_value=now_dt.day, min_value=1, max_value=31)),
                hour=self.get_datetime_unit_input(DatetimeUnit(name="hour", default_value=now_dt.hour, min_value=0, max_value=23)),
                minute=self.get_datetime_unit_input(DatetimeUnit(name="minutes", default_value=now_dt.minute, min_value=0, max_value=59)),
                second=self.get_datetime_unit_input(DatetimeUnit(name="seconds", default_value=now_dt.second, min_value=0, max_value=59))
            )
        except ValueError as e:
            print(e)
            exit()

    def get_datetime_unit_input(self, datetime_unit):
        datetime_unit_input = input(f"Enter a value for the {datetime_unit.get_name()}. ({datetime_unit.get_default_value()}) ")
        if (datetime_unit_input == ''):
            return datetime_unit.get_default_value()
        if (datetime_unit.is_valid(datetime_unit_input)):
            return int(datetime_unit_input)
        else:
            print(f"The value for the {datetime_unit.get_name()} must be an integer between {datetime_unit.get_min_value()} and {datetime_unit.get_max_value()}.")
            exit()
