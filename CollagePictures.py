# This script was originally accomplished with a .bat file named "Create - Pictures, Collage[jpg]" which is now in the Deprecated archive
# 	see that file for sources

# Resources
# 	https://github.com/ImageMagick/ImageMagick/discussions/4890

# Pre-requisites:
# 	ImageMagick
# 	PIL python module (Pillow)
print("* Pictures must not have spaces in their filenames")

import os
import re
import subprocess
from PIL import Image

# CONFIG =================================================================

inPath = "InputFolder"
outPath = "OutputFolder"

# FUNCTIONS ==============================================================

# Given a directory path (string), returns a list of filenames (strings) (with extensions)
def listFiles(dir):
	file_list = os.listdir(dir)
	return file_list

# Returns a files extension, including the dot
def extension(fileName):
	for ch in range(len(fileName)-1, -1, -1):
		if fileName[ch] == "." :
			return fileName[ch:]

	return "Error in 'extension' method"

# Returns a file title (filename without the extension)
def title(fileName):
	for ch in range(len(fileName)-1, -1, -1):
		if fileName[ch] == "." :
			return fileName[:ch]

	return "Error in 'title' method"

# Param: array of strings
# Return: array of strings
# source: https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort#answer-4836734
def natural_sort(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(l, key=alphanum_key)

# MAIN =================================================================

files = natural_sort(listFiles(inPath))

unacceptableExtension = False
for s in files:
	if not(extension(s) in [".jpg", ".jpeg", ".png", ".tiff"]):
		unacceptableExtension = True

if not(unacceptableExtension):
	# Get largest image dimensions from pictures in inPath
	maxWidth, maxHeight = 0, 0
	for s in files:
		im = Image.open(inPath+"\\"+s)
		width, height = im.size
		if width > maxWidth: maxWidth = width
		if height > maxHeight: maxHeight = height

	if len(files) < 4:
		maxWidth = ""

	command = "magick " + inPath+"\\*"
	command += " -gravity center -background none -extent " +str(maxWidth)+ "x" +str(maxHeight)+ " miff:- |" # Before montaging all the pictures, extend each image's tile, and center the image in that tile. then, pipe the the resulting images in 'miff' format to the montage command.
	command += " magick montage - +repage -background none -geometry +5+5"
	command += " " + outPath+"\\"+title(files[0])+"_montage.png"
	
	print(len(files), "files found in the input path. Largest dimensions (independantly searched for) are:", str(maxWidth)+"x"+str(maxHeight))
	print("The delivered command will be: \n\t" + command)

	print("\nDelivering command...", end=None)
	os.system(command)

	print("Done")
	os.system("PAUSE")

else:
	print("Files with unacceptable extensions in the input folder")
	os.system("PAUSE")
