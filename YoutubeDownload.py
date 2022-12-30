'''
Youtube Download.py [2022.12.14]
Downloads youtube videos using yt-dlp, with presets to speedy it up

Requirements:
	yt-dlp, added to PATH, or in the same folder as this script
'''

import subprocess
from types import SimpleNamespace

# CONFIG =================================

cfg = SimpleNamespace(**{
	"outPath": "OutputFolder\\",
	"testingMode": False
})

presets = [
	["yt-dlp", "-S", "vcodec:av1", "-P", "<outPath>", "-o", "%(title)s.%(ext)s", "<LINK>"],
	["yt-dlp", "-S", "res:1080,vcodec:av1", "--embed-chapters", "-P", "<outPath>", "-o", "%(title)s.%(ext)s", "<LINK>"],
	["yt-dlp", "-S", "res:1080,vcodec:av1", "--embed-chapters", "--sub-lang", "en", "--convert-subs", "srt", "--write-sub", "-P", "<outPath>", "-o", "%(title)s.%(ext)s", "<LINK>"],
	["yt-dlp", "-S", "res:1080,vcodec:h264", "-P", "<outPath>", "-o", "%(title)s.%(ext)s", "<LINK>"],
	["yt-dlp", "--extract-audio", "--add-metadata", "--audio-format", "opus", "-P", "<outPath>", "<LINK>"],
]

# FUNCTIONS ==============================

def sendCommand(command, placeholders):
	for i in range(len(command)):
		for key in placeholders:
			command[i] = command[i].replace(key, placeholders[key])

	print("Sending command: " + " ".join(command))
	try: subprocess.call(command)
	except Exception as e:
		print("Error:", e)
		return False

	return True

# MAIN ===================================

def displayPresets():
	print("PRESETS:")
	for i in range(len(presets)):
		print("\t" + str(i) + ")", " ".join(presets[i]))
displayPresets()

# Take input {
userInput = list()
print("\nProvide the youtube link (string), and the preset selection (int) (expected input format: <LINK> <PRESETSELECTION>)", end="\n")

if cfg.testingMode: userInput = ["https://www.youtube.com/watch?v=PnKgygXPxm4", "2"]
else:
	def input_isClean(_input): return (len(_input) == 2) and (_input[1].isnumeric()) and (int(_input[1]) >= 0 and int(_input[1]) < len(presets))

	while not input_isClean(userInput):
		userInput = input().split(" ")
		if not input_isClean(userInput): print("Bad input!", end="\n\n")	
# }

# Download video{
placeholders = {
	"<outPath>": cfg.outPath,
	"<LINK>": userInput[0]
}

sendCommand(command=presets[int(userInput[1])], placeholders=placeholders)
# }

input("Press <ENTER> to continue")