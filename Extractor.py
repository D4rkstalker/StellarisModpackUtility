import os, sys, re
# import glob
import subprocess
import shutil
from pathlib import Path

if 'posix' in sys.builtin_module_names:
	STEAM_PATH = "~/.steam"
else:
	import winreg
	STEAM_PATH = r"Software\Valve\Steam"
	STEAM_PATH = winreg.QueryValueEx(winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), STEAM_PATH), "SteamPath")[0]

if not STEAM_PATH:
   STEAM_PATH = "C:\\Program Files (x86)\\Steam" # Your Steam installation path goes here


def getWorkshopPath(SteamPath):
	SteamPath = Path(SteamPath) / "steamapps"
	if not SteamPath.is_dir():
		return

	workshop = SteamPath / "workshop"

	if not workshop.is_dir():
		workshop = SteamPath / "libraryfolders.vdf"
		if workshop.is_file():
			with open(str(workshop), "r", encoding="utf-8") as workshop:
				workshop = workshop.readlines()
				for l in workshop:
					l = re.search(r'\s*"1"\s*\"([^"]+)\"$', l)
					# if '	"1"		' in l:
					l = l and l.group(1) or None
					if l:
						workshop = Path(l) / "steamapps" / "workshop"
						break
				if type(workshop) is not list and workshop.is_dir():
					SteamPath = workshop
	else:
		SteamPath = workshop
	return SteamPath


def copyDirectory(src, dest):
	try:
		shutil.copytree(src, dest, ignore=shutil.ignore_patterns('*.zip'))
	except (shutil.Error, OSError) as e:
		print('Directory not copied. Error: %s' % e)

def getFiles(workshop): 
	"This will return absolute paths"
	if not workshop.is_dir():
		return
	directory = workshop / "content" / "281990"
	file_list = sorted(directory.glob("*/*.zip"))
	descriptor_list = sorted(directory.glob("*/descriptor.mod"))
	return file_list,descriptor_list

def unzip(src,dest):
	subprocess.call(["7z", "x",src, '-o' + dest])

STEAM_PATH = getWorkshopPath(STEAM_PATH)

if not STEAM_PATH:
	raise ValueError('No Steam workshop path found!')

whiteList = open('whitelist.txt','r').read()
whiteList = whiteList.split("\n")
files, descriptors = getFiles(STEAM_PATH)
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
