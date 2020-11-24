import glob
import os
import re
import collections
import json
import operator
import copy

files = []

def ModRelics():
    for file in files:
        f =  open(file, 'r',encoding='utf-8', errors = 'ignore')
        _file = f.read()
        f.close()
        text = ""
        out = []
        started = False
        for line in _file.split("\n"):
            if "{" in line:
                started = True
            if "#" in line:
                line = line.split("#")[0]
            if "@" in line and not started:
                out.append(line + "\n")
            text += line + "\n"
        #print(text)
        
        text = re.sub('\t*\n', '\n', text)
        text = re.sub(' *\n', '\n', text)
        #Special case for real space
        text = re.sub('с', 'c', text)
        
        relics = re.findall(r'\w*? *= {.*?\n}', text, re.DOTALL)
        for relic in relics:
            cooldown = False
            for line in relic.split("\n"):
                if "modifier = \"relic_activation_cooldown\"" in line:
                    cooldown = True
                if cooldown:
                    print(line)
                    if "days" in line:
                        cooldown = False
                    line = line.replace('days = @triumph_duration_veryshort', 'days = 360')
                    line = line.replace('days = @triumph_duration_short', 'days = 360')
                    line = line.replace('days = @triumph_duration', 'days = 360')
                    line = re.sub(r'days = \d*', 'days = 360', line)
                    
                out.append(line + "\n")
            out.append("\n")
        o = open(file,"w")
        
        for line in out:
            try:
                o.write(line)
            except Exception as e:
                
                print("\n-----")
                print(file)
                print(line)
                print(e)
                print("-----\n")
        o.close()




def parse_dir():
    global files
    target_dir = "mod\\! Modpack\\common\\relics"

    files += glob.glob(target_dir + '\\*.txt')


parse_dir()
ModRelics()
#genLeaderTraits(sortedTraits)
#for trait in alltraits:
    #print(json.dumps(trait.__dict__))
print("Done")
input()
