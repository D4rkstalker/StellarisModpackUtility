
# -*- coding: utf-8 -*-
#!python3.6
import json, os, sys, re
try: to_unicode = unicode
except NameError: to_unicode = str
from pathlib import Path
import tkinter as tk
from tkinter import messagebox 
import traceback
import emoji

mods_registry =  'mods_registry.json'
modList = [] # The modId order (game, which is in reverse to hashList)
# Check Stellaris settings location
settingPath = [	".", "..",
	os.path.join(os.path.expanduser('~'), 'Documents', 'Paradox Interactive', 'Stellaris'),
	os.path.join(os.path.expanduser('~'), '.local', 'share', 'Paradox Interactive', 'Stellaris')]
settingPath = [s for s in settingPath if os.path.isfile(os.path.join(s, mods_registry))]

if 'posix' in sys.builtin_module_names:
	STEAM_PATH = "~/.steam"
else:
	import winreg
	STEAM_PATH = r"Software\Valve\Steam"
	STEAM_PATH = winreg.QueryValueEx(winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), STEAM_PATH), "SteamPath")[0]

if not STEAM_PATH:
   STEAM_PATH = "C:\\Program Files (x86)\\Steam" # Your Steam installation path goes here

def mBox(type, text):
	tk.Tk().withdraw()
	style = not type and messagebox.showinfo or type == 'Abort' and messagebox.showwarning or messagebox.showerror
	style(title=type, message=text)

def abort(message):
	mBox('Abort', message)
	sys.exit(1)

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
	global mods_registry
	global modList
	mods_registry = Path(settingPath) /  mods_registry
	with mods_registry.open(encoding='UTF-8') as data:
		data = json.load(data)
		if not len(data):
			abort('No mod found!')
	modList = [d['displayName'].encode() for _, d in data.items() if 'displayName' in d]


def getWorkshopPath(STEAM_PATH):
	STEAM_PATH = Path(STEAM_PATH) / "steamapps"
	if not STEAM_PATH.is_dir():
		return
	workshop = STEAM_PATH / "workshop"
	if not workshop.is_dir():
		workshop = STEAM_PATH / "libraryfolders.vdf"
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
					STEAM_PATH = workshop
	else:
		STEAM_PATH = workshop
	return STEAM_PATH


def genModList(STEAM_PATH):
	STEAM_PATH = getWorkshopPath(STEAM_PATH)
	if not STEAM_PATH:
		return abort('No Steam workshop path found!')

	def _getFiles(workshop):
		"This will return absolute paths"
		if not workshop.is_dir():
			return
		file_list = workshop / "content" / "281990"
		file_list = sorted(file_list.glob("*"))
		return file_list

	files = _getFiles(STEAM_PATH)
	# print(type(files),len(files),*files, sep="\n")
	outlist = open('list.txt','w+')
	out = []
		
	for f in files:
		file = f / "descriptor.mod"
		# print(file)
		if not file or not file.exists():
			print(f, "no descriptor.mod found")
			file = next(f.glob("*.zip"), '')
			if file and file.exists():
				out.append(''.join(e for e in file.name.replace(".zip","") if e.isalnum()))
			else:
				f = str(f)
				print("Error: no valid mod file found!", f)
				#os.rmdir(f) # Empty dir
			continue

		descriptor = file.open(encoding="utf-8")
		contents = descriptor.readlines()
		for line in contents :
			if "name" in line:
				name = re.search(r'^name\s*=\s*\"?([^"]+)\"?$', line)
				name = name and name.group(1) or None
				if name:
					name = ''.join(e for e in name if e.isalnum())
					print(name, file.name)
					out.append(name.replace(".mod",""))
					break

	if len(out):
		out.sort()
		for item in out:
			try: 
				outlist.write("%s\n" % item)
			except: 
				print("-----ERRORED-----")
				print(item)
				print("-----------------")
			
		# outlist.write(json.dumps(out))
		outlist.close()
		#whitelist = open(os.path.join(settingPath, 'whitelist.txt'),'w+')


if True:
	#settingPath = settingPath[0]
	# print('Find Stellaris setting at %s' % settingPath)
	# try:
		# run(settingPath)
		genModList(STEAM_PATH)
		mBox('', 'done')

	# except Exception as e:
	# 	print(errorMesssage(e))
		#mBox('error', errorMesssage(e))
else:
	mBox('error', 'unable to locate "%s"' % mods_registry)

# print(type(modList),len(modList),*modList, sep="\n")

