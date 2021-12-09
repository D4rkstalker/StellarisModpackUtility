import os
import glob
import filecmp
import json
import whoosh
import sys

from whoosh.query import *
from whoosh.fields import Schema, TEXT
from shutil import copy2
from whoosh.index import create_in

def Conflict(file_path,entry):
    fname, extension = file_path[-1].split('.')
    file_path[-1] = fname + "." +  extension + " " + entry.strip() + "." +  extension
    file_path[0] = "mod/!conflicts!"
    print_conflict_path = os.sep.join(file_path[1:])
    print(f"Confict detected. Moving to !conficts!{os.sep}{print_conflict_path}.")
    return file_path


whitelist = open('whitelist.txt').read()
fileIndex = {}
whitelist = whitelist.split("\n")

schema = Schema(title=TEXT,content=TEXT)
if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)


# Set to true if updating a mod
override = False
while True:
    print("Auto-override unmarked files? (True/False) or (t/f) or (yes/no) or (y/n)")
    readin = input().lower()
    if readin in ['true', 'false', 't', 'f', 'yes', 'y', 'no', 'n']:
        if readin in ['true', 't', 'yes', 'y']:
            override = True
        break
for item in whitelist:
    entry = ''.join(e for e in item if e.isalnum())
    if entry == "":
        continue # Skip blank lines
    fileList = glob.glob('mod/'+entry.replace("\n","")+'/**',recursive=True)
    for filename in fileList:
        # Hack together the destination path
        file_path = str(filename).split(os.sep)
        path_within_mod = os.sep.join(file_path[1:])
        file_path[0] = "mod/! Modpack"
        name = str(filename)
        filePath = os.sep.join(file_path)
        # If this file exists in our modpack and has different contents, move it to the conflicts folder
        if os.path.isfile(filePath) and os.path.isfile(name) and not filecmp.cmp(filePath, name):
            # Check if file has been manually modified
            
            try:
                if ".txt" in filePath:
                    f = open(filePath,"r")
                    lines = f.readlines()
                    modification = lines[0]
                    f.close()
                    # Mark manually modified file with '#MODIFIED' as the first line, files not marked will be auto overriden
                    if override:
                        if "#MODIFIED" in modification:
                            file_path = Conflict(file_path,entry)
                        else:
                            #print("Overriding " + os.sep.join(file_path))
                            os.remove(os.sep.join(file_path))
                    else:
                        if "#MODIFIED" not in modification:
                            with open(filePath, "w") as dest:
                                dest.write("#MODIFIED\n")
                                dest.write("".join(lines))
                        file_path = Conflict(file_path,entry)
                else:
                    os.remove(os.sep.join(file_path))
    
            except Exception as e:
                try :
                    file_path = Conflict(file_path,entry)
                except Exception as e2:
                    print("/".join(file_path) + " Errored: " + str(e2))
        # Finalize our destination path
        filePath = os.sep.join(file_path)
        path = os.path.dirname(filePath)
        if not os.path.exists(path):
            os.makedirs(path)
        # Do not copy descriptor.mod, makes file explorer crash-y for some reason.
        if os.path.isfile(name) and ".mod" not in name and ".md" not in name:
            if path_within_mod in fileIndex:
                fileIndex[path_within_mod][0].append(entry.strip())
                fileIndex[path_within_mod][1] += 1
            else:
                fileIndex[path_within_mod] = [[entry.strip()], 0]
            copy2(name, filePath)

try:
    conflicts_list = dict()
    for i in fileIndex:
        if fileIndex[i][1]:
            conflicts_list[i] = fileIndex[i][0]
        fileIndex[i] = fileIndex[i][0]

    # Output a list of all files and a list of the conflicting files
    fileIndexOut = open("mod/!conflicts!/allFilesList.txt","w+")
    fileIndexOut.write(json.dumps(fileIndex, indent = 4))
    fileIndexOut.close()
    conflictsOut = open("mod/!conflicts!/conflictingFilesList.txt","w+")
    conflictsOut.write(json.dumps(conflicts_list, indent = 4))
    conflictsOut.close()
    print("Conflicting files listed in mod/!conflicts!/conflictingFilesList.txt")
except:
    print("No conflicts!")

if not os.path.isfile("mod/Modpack.mod"):
    descriptor = open("mod/Modpack.mod","w+")
    descriptor.write("""name=\"! Modpack"
path=\"mod/! Modpack\"
tags={
	\"Gameplay\"
}
supported_version=\"2.7.*\"""")
print("Done!")
input()
