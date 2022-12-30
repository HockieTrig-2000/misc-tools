import os
import re
import shutil

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
# via: https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort#answer-4836734
def natural_sort(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower()
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(l, key=alphanum_key)

def devFFmpegInputParam(files):

	inputParam = "concat:"+ files[0]
	for i in range(1, len(files), 1):
		inputParam += ("|"+ files[i])

	inputParam = '"'+ inputParam+ '"'
	return inputParam

# MAIN ================================================================
#print("List of files in InputFolder:")
files = listFiles("InputFolder")
#print(files)

#print("Naturally sorted list of files in InputFolder:")
files = natural_sort(files)
#print(files)

# Copy files with their new names into IntermediateFolder
sourceDir = os.getcwd()
#print("the source directory is: "+ sourceDir)
destinationDir = sourceDir+ "\\IntermediateFolder"
#print("the destination directory is: "+ destinationDir)

for i in range(0, len(files), 1):
	# source:
		# copying and renaming files: https://www.includehelp.com/python/copy-and-rename-files.aspx
		# adding padding to filenames: https://www.techiedelight.com/add-padding-number-python/
	shutil.copy("InputFolder\\"+ files[i], "IntermediateFolder\\"+ str(i+1).rjust(3, "0")+ extension(files[i]))

# Develop the FFmpeg command
	# Example structure: ffmpeg -i "concat:1.ts|2.ts|3.ts" -c copy output.ts
	# This uses the ffmpeg concat *protocol* as opposed to the concat demuxer, which shouldnt make the final video stutter between concatenations
files = listFiles("IntermediateFolder")
#print("Files in the intermediateFolder: ")
#print(files)

commandExtraParams = "-c copy"
#commandExtraParams = "-c:v libx265 -c:a aac -crf 24 -preset medium"

command = "ffmpeg -i "+ devFFmpegInputParam(files)+ " "+ commandExtraParams+ " "+ sourceDir+ "\\OutputFolder\\output.mp4"
print("The ffmpeg command will be: "+ command)

# Run command
os.system('cd IntermediateFolder & '+ command)

# Delete intermediate files
for st in files:
	os.remove("IntermediateFolder\\"+ st)

input("\nPress enter to exit")