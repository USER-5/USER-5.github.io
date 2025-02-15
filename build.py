#!/usr/bin/env python3
import os
from pathlib import Path
from shutil import copytree, rmtree

# I'm going to try to keep this to assembling files by concatenation
# Let's see how that goes...

this_script = Path(os.path.dirname(os.path.realpath(__file__)))
photos = this_script / "src/photos"
static = this_script / "src/static"
destination = this_script / "dist"
if(destination.exists()):
    rmtree(destination)

copytree(static, destination)

photos_page = ''
with open(photos / "container.html") as f:
    photos_page = f.read()

def is_valid_photo_date_folder(photo_date_folder: Path):
    return os.path.isdir(photo_date_folder) and os.path.isfile(photo_date_folder / "article.html")

photo_date_folders = (Path(photos/f) for f in os.listdir(photos) if is_valid_photo_date_folder(photos / f))

photos_page_content = ''
for photo_date_folder in photo_date_folders:
    with open(photo_date_folder / "article.html") as f:
        photos_page_content += f.read()

photos_page = photos_page.replace("<!-- !!Content!! -->", photos_page_content)

with open(destination / "photos.html", "w+") as f:
    f.write(photos_page)
