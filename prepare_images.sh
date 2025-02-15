#!/usr/bin/env bash

filename="$1"
basefilename=$(basename "${filename%.*}")

destination="$2"

if ! command -v magick; then
	echo "ERROR"
	echo "imagemagick is required. Try running from a nix shell:"
	echo "  nix-shell -p imagemagick"
	exit 1
fi

cp "$filename" "$destination"

for maxwidth in 650 1300 1950; do
	maxheight=$((maxwidth * 2))
	magick "$filename" -resize "${maxheight}x${maxwidth}" "$destination/$basefilename-$maxwidth".jpg
done
