#!/usr/bin/env bash

filename="$1"
basefilename=$(basename "${filename%.*}")

destination="$2"

if ! command -v magick > /dev/null; then
	echo "ERROR"
	echo "imagemagick is required. Try running from a nix shell:"
	echo "  nix-shell -p imagemagick"
	exit 1
fi

cp "$filename" "$destination"

for maxwidth in 400 650 700 800 850 900 1000 1200 1300 1950; do
	magick "$filename" -auto-orient -resize "${maxwidth}x" -quality 85 "$destination/$basefilename-$maxwidth".webp
done
