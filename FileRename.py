import os
import subprocess
import shutil
from datetime import date
import random

print("Rename Files.py v2022.11.19")

# CONFIG =================================================================

inPath = "InputFolder"
interPath = "IntermediateFolder"
outPath = "OutputFolder"
makeCopies = False

# STRUCTURES AND CLASSES =================================================

class Rename:
	class affix:
		# uses the user provided namingFormat to rename the files
		# returns True or False depending on the validity of the given namingFormat; if True, the files were renamed successfully
		def nf(self, namingFormat):
			requiredPlaceholders = ['%filename%', '%basename%', '%rand%']
			if len([v for v in requiredPlaceholders if v in namingFormat]) < 1: return False # input verification

			outFiles = [namingFormat] * len(files)
			
			for i in range(len(outFiles)):
				outFiles[i] = outFiles[i].replace("%filename%", files[i])
				outFiles[i] = outFiles[i].replace("%date%", today)
				outFiles[i] = outFiles[i].replace("%basename%", basename(files[i]))
				outFiles[i] = outFiles[i].replace("%ext%", extension(files[i]))
				outFiles[i] = outFiles[i].replace("%rand%", rand(8))

			execChanges(outFiles)
			return True

	class truncate:
		def str(self, keyword):
			outFiles = list(files)
			for i in range(len(outFiles)):
				outFiles[i] = basename(outFiles[i]).replace(keyword, "") + extension(outFiles[i]) # if the keyword happens to exist in the file's extension, don't truncate

			execChanges(outFiles)
			return True

		def rng(self, toRemove):
			print("havent coded this part yet")
			return True

	class replace:
		def str(self, strings):
			print("havent coded this part yet")
			return True

		def swu(self, strings):
			outFiles = list(files)
			for i in range(len(outFiles)):
				outFiles[i] = outFiles[i].replace(" ", "_")

			execChanges(outFiles)
			return True

		def num(self, increment):
			outFiles = list(files)
			for i in range(len(outFiles)):
				splitName = outFiles[i].split(" ")
				outFiles[i] = " ".join(
					list(
						[str(int(splitName[0]) + int(increment))])
						+ splitName[1:]
					)

			execChanges(outFiles)
			return True

commandTree = {
	'COMMANDS': {'OPTIONS': 'ARGUMENTS'},
	'-'*25: None,
	'affix': {
		'nf': 'Naming format that includes keywords (%filename%, %basename%, or %rand% is required)'
	},
	'truncate': {
		'str': 'String, whose every occurence in %basename% is deleted',
		'rng': 'Range, specifying characters to be truncated'
	},
	'replace': {
		'str': 'Old_string New_string',
		'swu': 'Spaces with underscores (no argument required)',
		"num": "Integer to be incremented to a filename's prepended number"
	}
}

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

	return ""

# Returns a file basename (filename without the extension)
def basename(fileName):
	for ch in range(len(fileName)-1, -1, -1):
		if fileName[ch] == "." :
			return fileName[:ch]

	return fileName

def rand(amtDigits):
	return "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(amtDigits))

# Prints multidimensional arrays nicely by indenting based on layer
def printArray(array, i = 0): # optional parameter 'i' specifies starting indentation layer. it is incremented as the function recurses
	for s in array:
		if isinstance(s, list): # https://stackoverflow.com/questions/26544091/checking-if-type-list-in-python
			printArray(s, i+1)
		else: print("\t"*i + s) # print as many tabs as is specified by 'i', then the object

# Similar to printArray, just for dictionaries
def printDict(dictionary, indentLevel = 0):
	for u in dictionary.keys():
		print('\t'*indentLevel + u)
		if type(dictionary[u]) == dict:
			printDict(dictionary[u], indentLevel+1)
		elif type(dictionary[u]) == str:
			print('\t'*(indentLevel+1) + dictionary[u])

def sW(body, w): return w + body + w

def execChanges(outFiles):
	if makeCopies:
		for i, s in enumerate(files):
			shutil.copyfile(inPath+"\\"+s, outPath+"\\"+outFiles[i])
		print(str(len(outFiles)) + " file(s) copied to outPath.")
	else:
		for i, s in enumerate(files):
			os.rename(inPath+"\\"+s, outPath+"\\"+outFiles[i])
		print(str(len(outFiles)) + " file(s) renamed to outPath")

# MAIN =================================================================

today = date.today().strftime("%Y.%m.%d") # 'today' is a string that contains the date in YYYY.MM.DD form
files = listFiles(inPath) # 'files' is an array of strings containing full-filenames in the input folder
print("Received", len(files), "file(s).")
print("makeCopies = " + str(makeCopies), end="\n\n")

keywords = ["%filename%", "%basename%", "%ext%", "%date%", "%rand%"]

if(len(files) > 0):
	# print commandTree and keywords
	printDict(commandTree)
	print("\nKEYWORDS:", end=" ")
	for s in keywords: print(s, end=" ")
	print()

	def badInput(errMsg=""): # local function for input verification
		if errMsg != "": errMsg = " (" + errMsg + ")"
		print("Bad input!!" + errMsg)

	# take input and rename files
	# the Rename() methods return error indications if any options or arguments given by the user are invalid
	while True:
		userInput = input("\nInput format: COMMAND OPTION ARGUMENT ").split(" ")
		userCommand, userOption, userArgument = '', '', ''
		try:
			userCommand = userInput[0]
			userOption = userInput[1]
			userArgument = " ".join(userInput[2:])
		except: pass

		# input verification
		if hasattr(Rename(), userCommand):
			method = getattr(Rename(), userCommand)
			if hasattr(method(), userOption):
				method = getattr(method(), userOption)
				if method(userArgument):
					break
				else: badInput("argument " + sW(userArgument, "\"") +" unacceptable"); continue
			else: badInput("option " + sW(userOption, "\"") +" not found"); continue
		else: badInput("command " + sW(userCommand, "\"") +" not found"); continue
		badInput(); continue

os.system("pause")