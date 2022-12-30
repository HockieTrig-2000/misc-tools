import os
import subprocess

# CONFIG ===============================

inPath = "InputFolder\\"
outPath = "OutputFolder\\"
interPath = "IntermediateFolder\\"

# FUNCTIONS ============================

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

def sW(body, wrap): return wrap + body + wrap

# MAIN =================================

fileList = listFiles(inPath)

for s in fileList:
	if(extension(s) == ".txt"):
		file1 = open(inPath + s, "r")
		lines1 = file1.readlines()

		with open(interPath + s, "w") as f:
			for i in range(len(lines1)):
				f.write(lines1[i])

				if lines1[i][-1:] != "\n": f.write("\n")
				f.write("\tout=" +  str(i) + ".ts\n")

		# command = ["aria2c", "-i", interPath + s, "-d", outPath]
		#command = ["aria2c", '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0', "-i", interPath + s, "-d", outPath]
		command = ["aria2c", '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', "-i", interPath + s, "-d", outPath]
		

		subprocess.call(command)

input("Press <ENTER> to continue")

# SOURCES =============================

'''
https://stackoverflow.com/questions/46102806/can-aria2c-download-list-of-urls-with-specific-file-names-for-each
'''