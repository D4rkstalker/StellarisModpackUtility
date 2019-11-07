#PATH = D:\Program Files (x86)\Steam\steamapps\workshop\content\281990
import os
import glob
import subprocess
import shutil
STEAM_PATH = "D:\\Program Files (x86)\\Steam" #Your steam installation path goes here

#For 2.3 - 
directory = STEAM_PATH + "\\steamapps\\workshop\\content\\281990\\**\\*.zip"

#For 2.4 +
directory2 = STEAM_PATH + "\\steamapps\\workshop\\content\\281990\\**\\*.mod"

def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

def getFiles(directory): 
    file_list = glob.glob(directory)
    descriptor_list = glob.glob(directory2)
    return file_list,descriptor_list

def unzip(src,dest):
    subprocess.call(["7z", "x",src, '-o' + dest])

whiteList = open('whiteList.txt','r').read()
whiteList = whiteList.split("\n")

files,descriptors = getFiles(directory)

#For 2.3-
for f in files: 
    for entry in whiteList:
        if "\\" + entry.strip() + ".zip" in f:
            fname = (f.split('\\'))[-1]
            unzip(f,'mod/' + ''.join(e for e in fname[:-4] if e.isalnum()))

#For 2.4+
for d in descriptors: 
    descriptor = open(d,"r").read()
    for entry in whiteList:
        if "name=\"" + entry + "\"" in descriptor:
            modDir = "\\".join(d.split("\\")[:-1])
            outDir = "mod/" + ''.join(e for e in entry if e.isalnum())
            print("Copying",entry)
            copyDirectory(modDir,outDir)
