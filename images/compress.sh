#!/usr/bin/env bash

if ! [ -f "$1" ]; then
	echo "File not found"
	exit 1
fi

filename="$1"
basename="${filename%.*}"

if ! command -v magick; then
	echo "ERROR"
	echo "imagemagick is required. Try running from a nix shell:"
	echo "  nix-shell -p imagemagick"
	exit 1
fi

for maxwidth in 650 1300 1950; do
	maxheight=$((maxwidth * 2))
	magick "$filename" -resize "${maxheight}x${maxwidth}" "$basename-$maxwidth".jpg
done
