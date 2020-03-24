#PATH = D:\Program Files (x86)\Steam\steamapps\workshop\content\281990
import os
import glob
import subprocess

directory = 'D:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\281990\\**\\*.zip'
directory2 = 'mod\\**\\*.mod'
def getFiles(directory): 
    
    # This will return absolute paths
    file_list = glob.glob(directory)
    descriptor_list = glob.glob(directory2)
    # for f in file_list: 
    #     print(f)
    return file_list,descriptor_list

whiteList = open('whiteList.txt','r').readlines()

files,descriptors = getFiles(directory)
outlist = open('descriptors.txt','w+')
out = []
# for f in files: 
#     print(f)
#     fname = (f.split('\\'))[-1]
#     out.append(fname)
for f in descriptors: 
    #print(f)
    
    descriptor = open(f,"r")
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