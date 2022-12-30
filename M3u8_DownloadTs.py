# Iterates through all .m3u8 files in inputFolder:
	# opens it in aria2 and downloads the individual .ts files to the outputFolder

import os
import subprocess

# CONFIG ===============================

inputFolder = "InputFolder"
outputFolder = "OutputFolder"

# FUNCTIONS ============================

def runCMD(command): os.system(command)

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

# MAIN =================================

bSlash = "\\"

inputFiles = listFiles(inputFolder)

for s in inputFiles:

	if(extension(s) == ".m3u8"):

		print("Processing:", s)
		subprocess.call(["aria2c", '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0', "-i", inputFolder+bSlash+s, "-d", outputFolder])

runCMD("PAUSE")