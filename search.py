import os
import glob
from shutil import copy2
import filecmp
#print("String to search: ")
THING_TO_SEARCH = "max_instances = 1"
# print("Directory to search: ")
# DIRECTORY_TO_SEARCH = input()

modFiles = glob.glob('mod\\! Modpack\\common\\solar_system_initializers\\**',recursive=True)
for _file in modFiles: 
	if os.path.isfile(_file):
		try:
			readFile = open(_file, "r",encoding="utf-8")
			#print(_file)
			if THING_TO_SEARCH in readFile.read():
				print("Found in: " + _file)
		except :
			print("Error while reading " + _file)
print("Done!")
input()