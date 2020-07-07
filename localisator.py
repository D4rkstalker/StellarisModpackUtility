## USAGE: You need install https://pyyaml.org/wiki/PyYAMLDocumentation for Python3.x
## ATTENTION: You must customize the vars localModPath and local_OVERHAUL
## TODO: Renaming (already translated) keys is not working
import os
import io
import tkinter as tk
from tkinter import messagebox
import traceback
# import sys
# import json
# from ruamel.yaml import YAML
# from ruamel.yaml.compat import StringIO
import yaml
import re
import glob
# yaml=YAML(typ='safe')

# Write here your mod folder name
localModPath = "ADeadlyTempest"
localizations = ["english", "german", "russian", "spanish", "braz_por", "french", "polish", "simp_chinese"]
local_OVERHAUL = ["spanish", "braz_por", "french", "polish"]
# localizations = ["english", "russian"]

# def abort(message):
# 	mBox('abort', message, 0)
# 	sys.exit(1)


def mBox(type, text):
	tk.Tk().withdraw()
	style = not type and messagebox.showinfo or type == 'Abort' and messagebox.showwarning or messagebox.showerror
	style(title=type, message=text)


def iBox(title, prefil, master):
	answer = filedialog.askdirectory(
		initialdir=prefil,
		title=title,
		parent=master)
	return answer

mods_registry = "mods_registry.json"

# Check Stellaris settings location
settingsPath = [
	".", "..",
	os.path.join(os.path.expanduser('~'), 'Documents', 'Paradox Interactive', 'Stellaris'),
	os.path.join(os.path.expanduser('~'), '.local', 'share', 'Paradox Interactive', 'Stellaris')
]
settingsPath = [s for s in settingsPath if os.path.isfile(os.path.join(s, mods_registry))]


if len(settingsPath):
	settingsPath = settingsPath[0]
else:
	from tkinter import filedialog
	mBox('Error', 'Unable to locate ' + mods_registry)
	settingsPath = iBox(
		"Please select the Stellaris settings folder:", settingsPath[0])

# mods_registry = os.path.join(settingsPath, mods_registry)

localModPath = os.path.join(settingsPath, "mod", localModPath, "localisation")

os.chdir(localModPath)

regRev1 =re.compile(r'^ +\"([^:"\s]+)\": ', re.MULTILINE)
regRev2 = re.compile(r'(?:\'|([^:"]{2}))\'?$', re.MULTILINE)

def tr(s):
	print(type(s),len(s))
	if type(s) is bytes: s = s.decode('utf-8')
	# s = re.sub('\n', '\\n', s)
	s = s.replace('\\n', 'BRR')
	# s = s.replace("\"", '”')
	s = s.replace("\'", '’')
	# s = s.replace(":", '…')
	# s = re.sub(r'\\n', '\\n', s)
	return re.sub(r':[0-2] ', ': ', s)


def trReverse(s):
	"Paradox workaround"
	print(type(s))
	if type(s) is bytes: s = s.decode('utf-8')
	s = s.replace('  ', ' ')
	s = re.sub(r'BRR *', r'\\n', s)
	s = re.sub(regRev1, r' \g<1>:0 ', s) # add 0 to keys
	s = re.sub(re.compile(r'^"(l_\S+)":\n'), r'\1:\n', s)
	# s = s.replace("”", "\"")
	s = s.replace("’", "\'")
	# s = s.replace("…", ':')
	# s = re.sub(regRev2, r'\1"', s)
	return s


def getYAMLstream(lang, filename):
	"Read YAML file"
	if lang != "english":
		filename = filename.replace("english", lang)
	lang = os.path.join(os.getcwd(), filename)
	# print(lang)
	if os.path.isfile(lang):
		return io.open(lang, "rb") #, encoding='utf-8-sig'


def writeStream(lang, stream, filename):
	"Write YAML file"
	filename = filename.replace("english", lang)
	if not os.path.isdir(lang):
		try:
			os.mkdir(lang)
		except OSError:
			print ("Creation of the directory %s failed" % lang)
		else:
			print ("Successfully created the directory %s " % lang)
	lang = os.path.join(os.getcwd(), filename)
	print(lang, os.path.isfile(lang))
	# if not os.path.isfile(lang):
	if type(stream) is bytes: stream = stream.decode('utf-8')
	with io.open(lang, 'w', encoding='utf-8-sig') as f:
		f.write(stream)
		# yaml.dump(stream, f, indent=1)

# yaml = ruamel.yaml.YAML(typ='safe')
yaml.default_flow_style = False
yaml.allow_unicode = True
# yaml.indent = 0
# yaml.allow_duplicate_keys = False
# if __name__ == '__main__':
# yaml.warnings({'YAMLLoadWarning': False})

#CrisisManagerEvent_l_english
for filename in glob.iglob(os.path.join('english','*.yml'), recursive=False):
	# print(filename)
	streamEn = getYAMLstream(localizations[0], filename)
	streamEn = streamEn.read()
	# print(streamEn)
	dictionary = {}
	# try:
	# 	print(type(dictionary),dictionary)
	# 	# print(dictionary["ï»¿l_english"])
	# except yaml.YAMLError as exc:
	# 	print(exc)
	# doc = yaml.load_all(stream, Loader=yaml.FullLoader)
	# doc = yaml.dump(dictionary) # ["\u00ef\u00bb\u00bfl_english"]
	# doc = json.dumps(dictionary) # ["\u00ef\u00bb\u00bfl_english"]
	# doc = yaml.dump(dictionary)
	# print(type(dictionary), dictionary)
	# doc = tr(dictionary['l_english'])
	# dictionary = yaml.load(tr(streamEn), Loader=yaml.FullLoader)
	dictionary = yaml.safe_load(tr(streamEn))
	# print("New document:", type(dictionary))
	doc = dictionary["l_english"]
	# print(type(doc), doc)
	# for doc in dictionary:
	for lang in range(1, len(localizations)):
		changed = False
		lang = localizations[lang]
		stream = getYAMLstream(lang, filename)
		if not stream:
			stream = {}
			print("Create new document "+lang)
			stream = streamEn.replace(b'l_english', bytes('l_'+lang, "utf-8"))
			# copy file with new header
			writeStream(lang, stream, filename)
			continue

		langStream = tr(stream.read())
		# print("Str document:", type(langStream), langStream)
		# langStream = yaml.load(langStream, Loader=yaml.FullLoader)
		langStream = yaml.safe_load(langStream)

		if not "l_"+lang in langStream:
			print("FAIL on file", filename.replace("english", lang), langStream)
			continue
		langDict = langStream["l_"+lang]
		#print("Dict document:", type(langStream), langStream)

		# for _, doc in dictionary.items():
		if type(doc) is dict and type(langDict) is dict:
			for key, value in doc.items():
				# print(key, value)
				if key not in langDict or (lang in local_OVERHAUL and langDict[key] != value):
					langDict[key] = value
					changed = True
					print("Fixed document " + filename.replace("english", lang), key, value)
					# break
				# else: print(bytes(key + ":0 " + langDict[key], "utf-8").decode("utf-8"))
			for key in list(langDict.keys()):
				if key not in doc:
					del langDict[key]
					changed = True
					print(key, "removed from document " + filename.replace("english", lang))

		if changed:
			# dictionary = doc.copy()
			# dictionary.update(langDict)
			# langStream["l_"+lang] = dictionary
			langStream["l_"+lang] = langDict
			# print(type(langStream), langStream)
			langStream = yaml.dump(langStream, width=10000, allow_unicode=True, indent=1, default_style='"') # , encoding='utf-8'
			langStream = trReverse(langStream)
			# print(type(langStream), langStream.encode("utf-8"))
			writeStream(lang, langStream, filename)
