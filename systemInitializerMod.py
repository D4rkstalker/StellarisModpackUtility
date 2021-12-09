import glob
import os
import re
import collections
import json
import operator
import copy

files = []

def ModSystems():
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
        
        systems = re.findall(r'\w*? *= {.*?\n}', text, re.DOTALL)
        for system in systems:
            unique = False
            spawnChance = False
            base = False
            if "usage_odds = {" in system:
                print(file)
            if "max_instances = 1\n" in system:
                unique = True
            if "spawn_chance = " in system:
                spawnChance = True
            if "usage_odds = " in system:
                base = True
            for line in system.split("\n"):
                if "spawn_chance = " in line and unique and spawnChance:
                    line = "\tspawn_chance = 9999"
                    #unique = False
                if "base = " in line and unique and base: 
                    line = "\t\tbase = 9999"
                    #print(file)
                    #base = False
                elif "usage_odds =" in line and "{" not in line and unique and base: 
                    line = "\tusage_odds = 9999"
                if "max_instances = 1" in line and not base:
                    out.append("\tusage_odds = 9999\n")
                if "max_instances = 1" in line and not spawnChance:
                    out.append("\tspawn_chance = 9999\n")
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
    target_dir = "mod\\! Modpack\\common\\solar_system_initializers"

    files += glob.glob(target_dir + '\\*.txt')


parse_dir()
ModSystems()
#genLeaderTraits(sortedTraits)
#for trait in alltraits:
    #print(json.dumps(trait.__dict__))
print("Done")
input()
