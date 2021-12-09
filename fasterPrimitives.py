import glob
import os
import re
import collections
import json
import operator
import copy

files = []

def ModPrimitives():
    for file in files:
        f =  open(file, 'r',encoding='utf-8', errors = 'ignore')
        _file = f.read()
        f.close()
        if "namespace = primitive" in _file:
            try:
                #print(file)
                replacer = re.findall(r"years = \d*",_file)
                replacer += re.findall(r"months = \d*",_file)
                replacer += re.findall(r"days = \d*",_file)
                
                for time in replacer:
                    t = int(time.split("=")[1])
                    tType = time.split("=")[0]
                    #print ( "|" + time + "|")
                    _file = _file.replace(time,tType + " = " + str(int(t/5)))
                o = open(file,"w")
                o.write(_file)
                o.close()
            except Exception as e:
                print(e,file)



def parse_dir():
    global files
    target_dir = "mod\\! Modpack\\events\\"

    files += glob.glob(target_dir + '\\*.txt')


parse_dir()
ModPrimitives()
#genLeaderTraits(sortedTraits)
#for trait in alltraits:
    #print(json.dumps(trait.__dict__))
print("Done")
input()
