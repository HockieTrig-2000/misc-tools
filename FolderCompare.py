'''
Folder_Compare.py [2022.12.30]

Compares contents within two directories, whose contents are specified in args.
'''

import os; os.system('cls' if os.name == 'nt' else 'clear')
import sys
from types import SimpleNamespace
import pprint

# CONFIG =================================================

cfg = SimpleNamespace(**{
	"recurseFolders": True, # doesnt do anything yet
	"testingMode": True,
	"verbosity": 3 # verbosity level (1-5, default 3)

})

# FUNCTIONS ==============================================

class G:
	# Given a directory path (string), returns a list of filenames (strings) (with extensions)
	def listFiles(dir):
		full_list = os.listdir(dir)
		return full_list

	# Returns a files extension, including the dot
	def extension(fileName):
		for ch in range(len(fileName)-1, -1, -1):
			if fileName[ch] == "." : return fileName[ch:]
		return ""

	# Returns a file title (filename without the extension)
	def basename(filename):
		for ch in range(len(filename)-1, -1, -1):
			if filename[ch] == "." : return filename[:ch]
		return filename

	def catchErr(situation = "Error", reason = ""):
		if reason == "": print(situation)
		else: print(situation + ":", reason)
		input("Press <ENTER> to exit")
		raise SystemExit

	def wrap(root, affix, closeBrackets=True):
		pairs = { "(": ")", "[": "]", "{": "}", "<": ">"}
		return affix + root + (pairs[affix] if (closeBrackets and (affix in pairs.keys())) else affix)

	def dict_toStr(dictionary, indent=2): return pprint.pformat(dictionary, sort_dicts=False, indent=indent)

	iife = lambda f: f()

class Tree:
	def makeTree(path):
		for root, dirs, files in os.walk(path, topdown=True): # walk through top-level folder (will not recurse, because of the return statement)
			return {
				"path": root,
				"name": root[root.rfind("\\") + 1 : ],
				"folders": [ # list of nodes (python dicts), each resembling another folder tree (this is the recursion step)
					Tree.makeTree(root + ("" if root[-1] == "\\" else "\\") + v)
					for v in dirs
					# Hidden folders which we dont want to be part of our tree: "$RECYCLE.BIN", "System Volume Information"
					if (v[0] != "$" and v != "System Volume Information") ],
				"files": files # simply a list of filenames
			}

	def dispTree(tree, indent=0):
		for s in tree["files"]: print("\t"*indent + s)
		if len(tree["files"]) > 0 and len(tree["folders"]) > 0: print()

		for i in range(len(tree["folders"])):
			print("\t"*indent + tree["folders"][i]["name"])
			Tree.dispTree(tree=tree["folders"][i], indent=indent+1)
			if len(tree["folders"][i]["files"]) > 0 and i < len(tree["folders"])-1: print()

	def disp_outstandingItems(tree_X, tree_Y):
		outstandingItems = Tree.findOutstanding(tree_X, tree_Y)

		print("Outstanding items in: " + tree_X["path"])
		print()
		Tree.dispTree(outstandingItems)

	# Recurses through folders (all layers) of tree_X, compares them to those in tree_Y, and returns a tree (each node (python dict) resembles a folder)
	def findOutstanding(tree_X, tree_Y): # returns a directory tree with all the outstanding items which are in tree X, but not in tree Y
		outstandingItems = {
			"path": None,
			"name": None,
			"folders": [],
			"files": []
		}

		# Find outstanding folders
		for i in range(len(tree_X["folders"])): # iterate through folders in tree_X
			flag_folderMatch = False

			for j in range(len(tree_Y["folders"])): # iterate through folders in tree_Y
				if tree_Y["folders"][j]["name"] == tree_X["folders"][i]["name"]: # "if a folder name match is found in tree_Y"
					flag_folderMatch = True
					outstandingItems_tmp = Tree.findOutstanding(tree_X["folders"][i], tree_Y["folders"][j]) # find outstanding items between the 2 folders

					if len(outstandingItems_tmp["folders"]) + len(outstandingItems_tmp["files"]) != 0: # "if folder contents dont match"
						outstandingItems_tmp["name"] = tree_X["folders"][i]["name"] # give the node a name 
						outstandingItems["folders"].append(outstandingItems_tmp) # append the node to the list of outstanding folders

					break

			if not flag_folderMatch: # "if the folder from tree_X isnt found in tree_Y"
				outstandingItems["folders"].append(tree_X["folders"][i])

		# Find outstanding files
		outstandingItems["files"] = [v for v in tree_X["files"] if v not in tree_Y["files"]]

		return outstandingItems

# MAIN =============================================================

userArgs = sys.argv[1:] # the first argument is always the absolute path of the python file
dirTree_A, dirTree_B = {}, {}

# Input verification
if len(userArgs) != 2: G.catchErr(reason="Wrong amount of arguments! (Example call: \"Folder_Compare.py \"PATH_A\" \"PATH_B\"\")")

# Read folder contents {
if cfg.testingMode:
	try:
		dirTree_A = Tree.makeTree(userArgs[0])
		dirTree_B = Tree.makeTree(userArgs[1])
	except Exception as e: G.catchErr(situation="Error when reading folder contents", reason=e)

else:
	dirTree_A = Tree.makeTree(userArgs[0])
	dirTree_B = Tree.makeTree(userArgs[1])
# }

if cfg.verbosity >= 4:
	print(G.dict_toStr(dirTree_A))
	print(G.dict_toStr(dirTree_B))

print("="*50)
Tree.disp_outstandingItems(dirTree_A, dirTree_B)
print("="*50)
Tree.disp_outstandingItems(dirTree_B, dirTree_A)
print("="*50)

input("Press <ENTER> to continue")
raise SystemExit

''' SOURCES ======================================================

https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
'''