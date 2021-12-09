import os
import glob
from shutil import copy2
import filecmp
#TheSleeperFallenHiveEmpire
MODS_TO_REMOVE = [
    "RealSpaceNewFrontiers",    
]
FORCE_REMOVE = False
if FORCE_REMOVE:
    print("Deleting conflicts")

for mod in MODS_TO_REMOVE:
    modFiles = glob.glob('mod/'+mod +'/**',recursive=True)
    conflictingFiles = []
    for _file in modFiles: 
        if os.path.isfile(_file):
            tempList = _file.split("\\")
            del tempList[0]
            files = '/'.join(map(str, tempList))
            #print(files)
            deleteDis = "mod/! Modpack/" + files
            try:
                if FORCE_REMOVE or filecmp.cmp(deleteDis,_file): 
                    if os.path.isfile(deleteDis):
                        print("deleting: " + deleteDis )
                        os.remove(deleteDis)
                else: 
                    conflictingFiles.append(deleteDis)
            except: 
                    print("Not found! : " + deleteDis)
for conflict in conflictingFiles:
    print ("conflicts: " + str(conflict))
print("Done!")
input()