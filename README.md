# Photo Date

Photo Date command line tools.

## Requirements

[Python](https://www.python.org/downloads/) and [pipenv](https://pipenv.pypa.io/en/latest/installation.html) installed on your machine.

## Installation

1. Download the repository.
1. Extract the .zip.
1. Run `pipenv install` in the root directory (where the `Pipfile` is found).
1. Install [ffmpeg](https://www.gyan.dev/ffmpeg/builds/) onto your machine by following [this guide](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/).
1. Run `pipenv shell` to start the virtual environment.
1. Run `python . --help` inside the virtual environment shell to view the command line documentation.

## Commands

### `edit`
Edit the Date Taken metadata of photos.
```bash
python . edit --files "YOUR FILE 1" "YOUR FILE 2"
```

### `rename`
Rename photos based on their date metadata. Generates a log after renaming all photos in a given directory.
```bash
python . rename --directory "YOUR DIRECTORY"
```
