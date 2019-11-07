import os
import glob
import filecmp
import json
from shutil import copy2
whitelist = open('whitelist.txt').read()
fileIndex = {}
whitelist = whitelist.split("\n")
for item in whitelist:
    entry = ''.join(e for e in item if e.isalnum())
    if not entry == "":
        fileList = glob.glob('mod/'+entry.replace("\n","")+'/**',recursive=True)
        for filename in fileList:
            #Hack together the destination path
            file_path = str(filename).split("\\")
            nameOfFile = str(filename).split("\\")[-1]
            file_path[0] = "mod/! Modpack"
            name = str(filename)
            filePath = '\\'.join(file_path)
            print(filename)
            #If this file exists in our modpack and has different contents, move it to the conflicts folder
            if os.path.isfile(filePath) and os.path.isfile(name) and not filecmp.cmp(filePath,name):
                file_path[-1] = file_path[-1] + " " + entry.strip() + ".txt"
                file_path[0] = "mod/!conflicts!"
            
            #Finalize our destination path
            filePath = '\\'.join(file_path)
            path = os.path.dirname(filePath)
            if not os.path.exists(path): 
                os.makedirs(path)
            #Do not copy descriptor.mod, makes file explorer crash-y for some reason 
            if os.path.isfile(name) and not os.path.isfile(filePath) and ".mod" not in name: 
                if nameOfFile in fileIndex:
                    fileIndex[nameOfFile] +=", " + entry.strip()
                else:
                    fileIndex[nameOfFile] = entry.strip()

                copy2(name,filePath)

try:
    #Out put a list of conflicting files 
    fileIndexOut = open("mod/!conflicts!/filesList.txt","w+")
    fileIndexOut.write(json.dumps(fileIndex,indent = 4))
    fileIndexOut.close()
except: 
    print("No conflicts!")

if not os.path.isfile("mod/Modpack.mod"): 
    descriptor = open("mod/Modpack.mod","w+")
    descriptor.write("""name=\"! Modpack"
path=\"mod/! Modpack\"
tags={
	\"Gameplay\"
}
supported_version=\"2.5.*\"""")