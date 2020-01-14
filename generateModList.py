import os
import glob
import subprocess

STEAM_PATH = "D:\\Program Files (x86)\\Steam"   #Your steam installation path goes here

#For 2.3 - 
directory = STEAM_PATH + "\\steamapps\\workshop\\content\\281990\\**\\*.zip"

#For 2.4 +
directory2 = STEAM_PATH + "\\steamapps\\workshop\\content\\281990\\**\\*.mod"

def getFiles(directory): 
    
    # This will return absolute paths
    file_list = glob.glob(directory)
    descriptor_list = glob.glob(directory2)
    # for f in file_list: 
    #     print(f)
    return file_list,descriptor_list

files,descriptors = getFiles(directory)
outlist = open('list.txt','w+')
out = []
for f in files: 
    print(f)
    fname = (f.split('\\'))[-1]
    out.append(fname)
for f in descriptors: 
    #print(f)
    
    descriptor = open(f,"r", encoding="utf-8")
    contents = descriptor.readlines()
    for line in contents :
        if "name" in line: 
            name = line.replace("name=\"","").replace("\"","")
            print(name.strip(),f)
            out.append( name.strip())

out.sort()
for item in out:
    outlist.write((item.replace(".mod","").replace(".zip","") + '\n'))
outlist.close()
whitelist = open('whitelist.txt','w+')