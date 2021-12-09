import os, sys, re
# import glob
import subprocess
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import messagebox 
import traceback

if 'posix' in sys.builtin_module_names:
	STEAM_PATH = "~/.steam"
else:
	import winreg
	STEAM_PATH = r"Software\Valve\Steam"
	STEAM_PATH = winreg.QueryValueEx(winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), STEAM_PATH), "SteamPath")[0]

if not STEAM_PATH:
   STEAM_PATH = "C:\\Program Files (x86)\\Steam" # Your Steam installation path goes here

# Check Stellaris settings location
settingPath = [	".", "..",
	os.path.join(os.path.expanduser('~'), 'Documents', 'Paradox Interactive', 'Stellaris'),
	os.path.join(os.path.expanduser('~'), '.local', 'share', 'Paradox Interactive', 'Stellaris')]
settingPath = [s for s in settingPath if os.path.isfile(os.path.join(s, 'mods_registry.json'))]

def mBox(type, text):
	tk.Tk().withdraw()
	style = not type and messagebox.showinfo or type == 'Abort' and messagebox.showwarning or messagebox.showerror
	style(title=type, message=text)

def getWorkshopPath(SteamPath):
	SteamPath = Path(SteamPath) / "steamapps"
	if not SteamPath.is_dir():
		return
	workshop = SteamPath / "workshop"
	if not workshop.is_dir():
		workshop = SteamPath / "libraryfolders.vdf"
		if workshop.is_file():
			with workshop.open(encoding="utf-8") as workshop:
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
		if os.path.exists(dest):
			print(dest + " already exists, deleting")
			shutil.rmtree(dest)
		shutil.copytree(src, dest, ignore=shutil.ignore_patterns('*.zip'))
	except (shutil.Error, OSError) as e:
		print('Directory not copied. Error: %s' % e)

def getFiles(workshop): 
	"This will return absolute paths"
	if not workshop.is_dir():
		return
	workshop = workshop / "content" / "281990"
	files = sorted(workshop.glob("*/*.zip"))
	descriptors = sorted(workshop.glob("*/descriptor.mod"))
	return files, descriptors

def unzip(src,dest):
	if os.path.exists(dest):
		print(dest + " already exists, deleting")
		shutil.rmtree(dest)
	subprocess.call(["7z", "x",src, '-o' + dest])

STEAM_PATH = getWorkshopPath(STEAM_PATH)

if not STEAM_PATH:
	raise ValueError('No Steam workshop path found!')

def errorMesssage(error):
	error_class = e.__class__.__name__  # Get error type
	detail = e.args[0]  # Get details
	_, _, tb = sys.exc_info()   # Get Call Stack
	lastCallStack = traceback.extract_tb(tb)[-1]  # Get the last call from Call Stack
	fileName = lastCallStack[0] # Get the name of the file that happened
	lineNum = lastCallStack[1]  # Get the occurrence of the line number
	funcName = lastCallStack[2] # Get the name of the function that happened
	return "File \"{}\", line {}, in {}: [{}] {}".format(
		fileName, lineNum, funcName, error_class, detail)
	
def run(settingPath):
	whiteList = open(os.path.join(settingPath, 'whitelist.txt')).read()
	whiteList = whiteList.split("\n")
	files, descriptors = getFiles(STEAM_PATH)
	#For 2.4+
	for d in descriptors:
		for i in range(len(whiteList)-1,-1,-1):
			try:
				descriptor = d.open().read()
			except Exception as e: 
				print(e, " Using utf-8 charset", d)
				descriptor = d.open(encoding="utf-8").read()
			descriptor = ''.join(e for e in descriptor if e.isalnum())
			entry = whiteList[i]
			if entry in descriptor:
				outDir = os.path.join(settingPath, 'mod', ''.join(e for e in entry if e.isalnum()))
				print("Copying", entry)
				whiteList.remove(entry)
				copyDirectory(d.parents[0], outDir)
				# break
	#For 2.3-
	for entry in whiteList:
		for f in files:
			#print(f.name,entry)
			if ''.join(e for e in (f.name.replace(".zip","")) if e.isalnum()) == entry:
				#print(entry, f.name)
				unzip(f, os.path.join(settingPath, 'mod', ''.join(e for e in (f.name.replace(".zip","")) if e.isalnum()) ))
				break
	

if len(settingPath) > 0:
	settingPath = settingPath[0]
	# print('Find Stellaris setting at %s' % settingPath)
	try:
		run(settingPath)
		print("done")
	except Exception as e:
		print(errorMesssage(e))
		mBox('error', errorMesssage(e))
else:
	mBox('error', 'unable to locate the settings path.')

input()





