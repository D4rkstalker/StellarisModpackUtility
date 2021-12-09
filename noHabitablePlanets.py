import glob
import os
import re
import collections
import json
import operator
import copy


def ModPlanets(planet_files):
   
    for file in planet_files:
        f =  open(file, 'r',encoding='utf-8', errors = 'ignore')
        _file = f.read()
        f.close()
        with open(file, 'w') as o:
            firstPass = ""
            started = False
            for line in _file.split("\n"):
                if "#" in line:
                    line = line.split("#")[0]
                if "{" in line:
                    started = True
                if "@" in line and not started :
                    o.write(line + "\n")
                firstPass += line + "\n"
                
            planets = re.findall(r'\w*? = {.*?\n}', firstPass, re.DOTALL)
            for planet in planets:
                #if "colonizable = yes" in planet :
                    #print(planet)
                replacer = re.findall(r"spawn_odds = [0-9]*[.,]?[0-9]*",_file)
                for spawn in replacer:
                    planet = planet.replace(spawn,"spawn_odds = 0")
               
                o.write(planet)
                o.write("\n")
        

def ModInits(sol_files):
    for file in sol_files:
        f =  open(file, 'r',encoding='utf-8', errors = 'ignore')
        _file = f.read()
        f.close()
        if "class = rl_habitable_normal" in _file or "class = pc_nuked" in _file or "class = \"rl_habitable_normal\"" in _file or "class = \"pc_nuked\"" in _file:
            with open(file, 'w') as o:
                firstPass = ""
                started = False
                for line in _file.split("\n"):
                    if "#" in line:
                        line = line.split("#")[0]
                    if "{" in line:
                        started = True
                    if "@" in line and not started :
                        o.write(line + "\n")
                    firstPass += line + "\n"
                    
                systems = re.findall(r'\w*? = {.*?\n}', firstPass, re.DOTALL)
                for system in systems:
                    if "primitive" not in system and "starting_planet" not in system:
                        system = system.replace("rl_habitable_normal","rl_unhabitable_planets")
                        system = system.replace("pc_nuked","rl_unhabitable_planets")
                
                    o.write(system)
                    o.write("\n")



def parse_dir():
    planet_files = []
    sol_files = []
    target_dir = "mod\\! Modpack\\common\\star_classes\\"

    planet_files += glob.glob(target_dir + '\\*.txt')

    target_dir = "mod\\! Modpack\\common\\solar_system_initializers\\"
    sol_files += glob.glob(target_dir + '\\*.txt')
    ModPlanets(planet_files)
    ModInits(sol_files)




parse_dir()
#genLeaderTraits(sortedTraits)
#for trait in alltraits:
    #print(json.dumps(trait.__dict__))
print("Done")
input()
