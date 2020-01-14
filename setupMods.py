import glob
import os
from shutil import copy2

def setUpDescriptor(file_list):
    for descriptor in file_list: 
        copy2(descriptor, 'mod\\')
        newLocation = 'mod\\' + descriptor.split("\\")[1] + '.mod'
        print(newLocation)
        descriptorFile = open('mod\\descriptor.mod','r')
        contents = descriptorFile.readlines()
        out = ''
        print (contents)
        for line in contents: 
            if "archive" in line: 
                out += 'path="mod/' + descriptor.split("\\")[1] + '"\n'
            elif "name" in line: 
                out += 'name="_MODDED - ' +line[6:-1]+'\n'
            else: 
                out += line
        descriptorFile.close()
        descriptorFile = open('mod\\descriptor.mod','w')
        descriptorFile.write(out)
        descriptorFile.close()
        os.rename('mod\\descriptor.mod',newLocation)

whitelist = open('list.txt').read()
whitelist = whitelist.split("\n")
for item in whitelist: 
    entry = ''.join(e for e in item if e.isalnum())
    descriptorList = glob.glob("mod\\"+entry.replace("\n","")+"\\*.mod")
    setUpDescriptor(descriptorList)

