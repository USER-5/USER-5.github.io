#!/usr/bin/env python3
import os
from pathlib import Path
from shutil import copytree, rmtree
from subprocess import call
from glob import glob
from urllib.parse import quote
import sys

# I'm going to try to keep this to assembling files by concatenation
# Let's see how that goes...

# If set, don't rebuild everything from scratch
refresh = len(sys.argv) > 1 and  sys.argv[1] == "refresh"

print("Preparing directories")
this_script = Path(os.path.dirname(os.path.realpath(__file__)))
photos = this_script / "src/photos"
programming = this_script / "src/programming"
static = this_script / "src/static"
destination = this_script / "dist"
if destination.exists() and not refresh:
    rmtree(destination)

if not refresh:
    copytree(static, destination)

os.makedirs(destination / "images", exist_ok=True)
os.makedirs(destination / "programming", exist_ok=True)

print("Building photos page")
photos_page = ''
with open(photos / "container.html") as f:
    photos_page = f.read()

def is_valid_photo_date_folder(photo_date_folder: Path):
    return os.path.isdir(photo_date_folder) and os.path.isfile(photo_date_folder / "article.html")

photo_date_folders = [Path(photos/f) for f in os.listdir(photos) if is_valid_photo_date_folder(photos / f)]
photo_date_folders.sort()
photo_date_folders.reverse()

photos_page_content = ''
for photo_date_folder in photo_date_folders:
    print(f" Processing {photo_date_folder}")
    for image in glob(f"{photo_date_folder}/images/*.jpg"):
        if refresh and (destination / "images" / Path(image).name).exists():
            print(f"  Skipping image {image}")
            continue
        print(f"  Converting image {image}")
        call([this_script / 'prepare_images.sh',  image, destination / "images"])

    print("  Reading article")
    with open(photo_date_folder / "article.html") as f:
        photos_page_content += "<article>"
        photos_page_content += f.read()
        photos_page_content += "</article>"

photos_page = photos_page.replace("<!-- !!Content!! -->", photos_page_content)

print("Writing photos page")
with open(destination / "photos.html", "w+") as f:
    f.write(photos_page)

print("Building programming page")
programming_page = ''
with open(programming / "container.html") as f:
    programming_page = f.read()

programming_folders = [Path(programming/f) for f in os.listdir(programming) if Path(programming/f).is_dir()]
programming_folders.sort()
programming_folders.reverse()

programming_index_content = '<h2>Articles:</h2><ul>'
for programming_folder in programming_folders:
    article_title = programming_folder.stem
    article_filepath = "/programming/" + quote(article_title) + ".html"
    programming_index_content += f'<li><a href="{quote(article_filepath)}">{article_title}</a></li>'

    print(f" Processing {programming_folder} ({article_title})")

    print("  Reading article")
    programming_page_content = ''
    for article in glob(str(programming_folder) + "/*.html"):
        with open(article) as f:
            programming_page_content += "<article>"
            programming_page_content += f.read()
            programming_page_content += "</article>"
    programming_page_content = programming_page.replace("<!-- !!Content!! -->", programming_page_content)

    print("  Writing article page")
    with open(str(destination) + article_filepath, "w+") as f:
        f.write(programming_page_content)

programming_index_content += '</ul>'
programming_index_page = programming_page.replace("<!-- !!Content!! -->", programming_index_content)

print("Writing article page")
with open(destination / "programming.html", "w+") as f:
    f.write(programming_index_page)

