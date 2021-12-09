import glob
import os
import re
import collections
import json
import operator
import copy

files = []

def ModShipScales():
    for file in files:
        scale = "scale = 1.0"
        skip = False
        if "01_captainx3_entities_Battlecruiser" in file:
             scale = "\tscale = 0.45"
        elif "01_captainx3_entities_Carrier" in file:
             scale = "\tscale = 0.5"
        elif "01_captainx3_entities_Dreadnought" in file:
             scale = "\tscale = 0.5"
        elif "01_captainx3_entities_escortcarrier" in file:
             scale = "\tscale = 0.4"
        elif "01_captainx3_entities_explorationship" in file:
             scale = "\tscale = 0.4"
        elif "01_captainx3_entities_Flagship" in file:
             scale = "\tscale = 1"
        elif "01_captainx3_entities_StrikeCruiser" in file:
             scale = "\tscale = 0.4"
        else:
            #print("passing " + file)
            skip = True
        if not skip:
            f =  open(file, 'r',encoding='utf-8', errors = 'ignore')
            _file = f.read()
            f.close()
            replacer = re.findall(r"\tscale = \d\.?\d*",_file)
            #replacer += re.findall(r"\tscale = @\w*_scale ",_file)
            print(replacer)
            for rscale in replacer:
                _file = _file.replace(rscale, scale)
            with open(file,'w') as out:
                print(file)
                out.write(_file)



def parse_dir():
    global files
    target_dir = "mod\\! Modpack\\gfx\\models\\ships\\**"

    files += glob.glob(target_dir + '\\*.asset')


parse_dir()
ModShipScales()
#genLeaderTraits(sortedTraits)
#for trait in alltraits:
    #print(json.dumps(trait.__dict__))
print("Done")
input()
