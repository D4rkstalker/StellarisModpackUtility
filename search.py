import os
import glob
from shutil import copy2
import filecmp
print("String to search: ")
THING_TO_SEARCH = input()
# print("Directory to search: ")
# DIRECTORY_TO_SEARCH = input()
modFiles = []
# modFiles += glob.glob('mod\\\! Modpack\\localisation\\english\\**',recursive=True)
modFiles += glob.glob('mod\\\! Modpack\\common\\**',recursive=True)
modFiles += glob.glob('mod\\\! Modpack\\events\\**',recursive=True)
# modFiles += glob.glob('mod\\\! Modpack 2.8\\localisation\\english\\**',recursive=True)
for _file in modFiles: 
	if os.path.isfile(_file) and ".txt" in _file:
		try:
			readFile = open(_file, "r",encoding="utf-8")
			#print(_file)
			if THING_TO_SEARCH in readFile.read():
				print("Found in: " + _file)
		except :
			continue
			#print("Error while reading " + _file)
print("Done!")
input()