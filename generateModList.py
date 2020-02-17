# -*- coding: utf-8 -*-
#!python3.6
import json, os, sys, re
try: to_unicode = unicode
except NameError: to_unicode = str
from pathlib import Path
import tkinter as tk
from tkinter import messagebox 
import traceback

mods_registry =  'mods_registry.json'
modList = [] # the modId order (game, which is in reverse to hashList)
# check Stellaris settings location
settingPath = [
	".", "..",
	os.path.join(os.path.expanduser('~'), 'Documents', 'Paradox Interactive',
				 'Stellaris'),
	os.path.join(os.path.expanduser('~'), '.local', 'share',
				 'Paradox Interactive', 'Stellaris')
]
settingPath = [s for s in settingPath if os.path.isfile(os.path.join(s, mods_registry))]

if 'posix' in sys.builtin_module_names:
	SteamPath = "~/.steam"
else:
	import winreg
	SteamPath = r"Software\Valve\Steam" #SteamPath
	# "D:\\Program Files (x86)\\Steam"   #Your steam installation path goes here
	SteamPath = winreg.QueryValueEx(winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), SteamPath), "SteamPath")[0]

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
	_, _, tb = sys.exc_info()  # Get Call Stack
	lastCallStack = traceback.extract_tb(tb)[-1]  # Get the last call from Call Stack
	fileName = lastCallStack[0]  # Get the name of the file that happened
	lineNum = lastCallStack[1]  # Get the occurrence of the line number
	funcName = lastCallStack[2]  # Get the name of the function that happened
	return "File \"{}\", line {}, in {}: [{}] {}".format(
		fileName, lineNum, funcName, error_class, detail)


def run(settingPath):
	global mods_registry
	global modList
	mods_registry = os.path.join(settingPath, mods_registry)
	with open(mods_registry, encoding='UTF-8') as data:
		data = json.load(data)
		if not len(data):
			abort('No mod found!')
	modList = [d['displayName'].encode() for _, d in data.items() if 'displayName' in d]


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
					if l:
						workshop = l and l.group(1) or None
						if workshop:
							workshop = Path(workshop) / "steamapps" / "workshop"
							break
				if type(workshop) is not list and workshop.is_dir():
					SteamPath = workshop
	else:
		SteamPath = workshop
	return SteamPath


def genModList(SteamPath):

	SteamPath = getWorkshopPath(SteamPath)
	if not SteamPath:
		return abort('No path found!')

	def _getFiles(workshop):
		"This will return absolute paths"
		if not workshop.is_dir():
			return
		file_list = workshop / "content" / "281990"
		file_list = sorted(file_list.glob("*"))
		return file_list

	files = _getFiles(SteamPath)
	# print(type(files),len(files),*files, sep="\n")
	outlist = open(os.path.join(settingPath, 'list.txt'),'w+')
	out = []
		
	for f in files:
		file = f / "descriptor.mod"
		# print(file)
		if not file or not file.exists():
			print(f, "no descriptor.mod found")
			file = next(f.glob("*.zip"), '')
			if file and file.exists():
				out.append(file.name.replace(".zip",""))
			else:
				f = str(f)
				print("Error: no valid mod file found!", f)
				os.rmdir(f)
			continue

		descriptor = open(str(file),"r", encoding="utf-8")
		contents = descriptor.readlines()
		for line in contents :
			if "name" in line:
				name = re.search(r'^name\s*=\s*\"?([^"]+)\"?$', line)
				name = name and name.group(1) or None
				if name:
					print(name, file.name)
					out.append(name.replace(".mod",""))
					break

	if len(out):
		out.sort()
		for item in out:
			outlist.write("%s\n" % item)
		# outlist.write(json.dumps(out))
		outlist.close()
		whitelist = open(os.path.join(settingPath, 'whitelist.txt'),'w+')


if len(settingPath) > 0:
	settingPath = settingPath[0]
	print('Find Stellaris setting at %s' % settingPath)
	try:
		# run(settingPath)
		genModList(SteamPath)
		mBox('', 'done')

	except Exception as e:
		print(errorMesssage(e))
		mBox('error', errorMesssage(e))
else:
	mBox('error', 'unable to locate "%s"' % mods_registry)

# print(type(modList),len(modList),*modList, sep="\n")