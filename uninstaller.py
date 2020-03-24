import os
import glob
from shutil import copy2
import filecmp

MOD_TO_REMOVE = "EnhancedTraits"

modFiles = glob.glob('mod/'+MOD_TO_REMOVE +'/**',recursive=True)
conflictingFiles = []
for _file in modFiles: 
    if os.path.isfile(_file):
        tempList = _file.split("\\")
        del tempList[0]
        files = '/'.join(map(str, tempList))
        print(files)
        deleteDis = "mod/! Modpack/" + files
        try:
            if filecmp.cmp(deleteDis,_file): 
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