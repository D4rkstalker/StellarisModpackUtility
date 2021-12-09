import glob
import os
import re
import collections
import json
import operator
import copy

files = []

def ModDeposits():
    try:
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
            if "@Orbital_deposit_boosted = 1" not in text:
                out.append("@Orbital_deposit_boosted = 1\n")
                text = re.sub('\t*\n', '\n', text)
                text = re.sub(' *\n', '\n', text)
                #text = re.sub('{ ', '{\n', text)
                #text = re.sub(' }', '\n}', text)
                
                deposits = re.findall(r'\w*? *= {.*?\n}', text, re.DOTALL)
                for deposit in deposits:
                    hasDeposit = False
                    produces = False
                    for line in deposit.split("\n"):
                        if ("}" in line or "{" in line) and produces:
                            produces = False
                            hasDeposit = False
                        if produces:
                            parts = line.split("=")
                            temp = float(parts[1])
                            line = parts[0] + " = " + str(temp * 2)
                        if "category = orbital_mining_deposits" in deposit or "category = orbital_mining_deposits" in deposit:
                            hasDeposit = True
                        if "produces = {" in line and hasDeposit:
                            produces = True
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
            else:
                print("patch already applied to " + file + "!, skipping")
    except Exception as e:
        print("\n-----")
        print(file)
        print(e)
        print("-----\n")




def parse_dir():
    global files
    target_dir = "mod\\! Modpack\\common\\deposits"

    files += glob.glob(target_dir + '\\*.txt')


parse_dir()
ModDeposits()
#genLeaderTraits(sortedTraits)
#for trait in alltraits:
    #print(json.dumps(trait.__dict__))
print("Done")
input()
