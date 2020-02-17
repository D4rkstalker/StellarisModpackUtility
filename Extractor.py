#PATH = D:\Program Files (x86)\Steam\steamapps\workshop\content\281990
import os, sys, re
# import glob
import subprocess
import shutil
from pathlib import Path

if 'posix' in sys.builtin_module_names:
	STEAM_PATH = "~/.steam"
else:
	import winreg
	STEAM_PATH = r"Software\Valve\Steam" #STEAM_PATH
	# "D:\\Program Files (x86)\\Steam"   #Your steam installation path goes here
	STEAM_PATH = winreg.QueryValueEx(winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), STEAM_PATH), "SteamPath")[0]

if not STEAM_PATH:
   STEAM_PATH = "C:\\Program Files (x86)\\Steam" #Your steam installation path goes here


def getWorkshopPath(workshop):
	workshop = Path(workshop)
	if not workshop.is_dir():
		return
	with open(str(workshop / "steamapps" / "libraryfolders.vdf"), "r", encoding="utf-8") as workshop:
		workshop = workshop.readlines()
		for l in workshop:
			if re.search(r'^\s*\"1\"\s*', l):
				l = re.search(r'\s*"1"\s*\"([^"]+)\"$', l)
				workshop = l and l.group(1) or None
				if workshop:
					break

		if type(workshop) is not list:
			workshop = Path(workshop)
			if workshop.is_dir():
				return workshop


def copyDirectory(src, dest):
	try:
		shutil.copytree(src, dest)
	except shutil.Error as e:
		print('Directory not copied. Error: %s' % e)
	except OSError as e:
		print('Directory not copied. Error: %s' % e)

def getFiles(directory): 
	directory = Path(directory) / "steamapps\\workshop\\content\\281990"
	file_list = sorted(directory.glob("*/*.zip"))
	descriptor_list = sorted(directory.glob("*/descriptor.mod"))
	return file_list,descriptor_list

def unzip(src,dest):
	subprocess.call(["7z", "x",src, '-o' + dest])

STEAM_PATH = getWorkshopPath(STEAM_PATH)

whiteList = open('whiteList.txt','r').read()
whiteList = whiteList.split("\n")

# print(type(whiteList),len(whiteList), whiteList)
files, descriptors = getFiles(STEAM_PATH)
# print(type(descriptors),len(descriptors), descriptors)
#For 2.4+
for d in descriptors: 
	try:
		descriptor = open(str(d),"r").read()
	except Exception as e: 
		print(e, " Using utf-8 charset", d)
		descriptor = open(str(d),"r", encoding="utf-8").read()
	for entry in whiteList:
		if "name=\"" + entry + "\"" in descriptor:
			# modDir = "\\".join(d.split("\\")[:-1])
			modDir = d.parents[0]
			outDir = "mod/" + ''.join(e for e in entry if e.isalnum())
			print("Copying", entry)
			whiteList.remove(entry)
			copyDirectory(modDir,outDir)

#For 2.3-
for f in files: 
	for entry in whiteList:
		if entry + ".zip" == f.name:
			print(entry, f.name)
			unzip(f,'mod/' + ''.join(e for e in str(f) if e.isalnum()))
