import os
import glob
import json
import filecmp
from shutil import copy2
#from filecmp import cmp as compare
from argparse import ArgumentParser
from make_mod_patch import mod_patch

def InitMerge(baseLineExists, forceMerge):
    print("\nAssembling modpack...")
    patchedFiles = open('whitelist.txt').read()
    whitelist = open('whitelist.txt').readlines()

    if not os.path.exists("index"):
        os.mkdir("index")
    #whitelist = whitelist.split("\n")

    # Set to true if updating a mod
    for entry in whitelist:
        
        #entry = ''.join(e for e in item if e.isalnum())
        print(entry)
        if entry == "":
            continue # Skip blank lines
        fileList = glob.glob('mod/'+entry.replace("\n","")+'/**',recursive=True)
        for filename in fileList:
            # Hack together the destination path
            file_path = str(filename).split(os.sep)
            path_within_mod = os.sep.join(file_path[1:])
            file_path[0] = "mod/! Modpack"
            name = str(filename)
            filePath = os.sep.join(file_path)

            # If this file exists in our modpack and has different contents, move it to the conflicts folder
            if os.path.isfile(filePath) and os.path.isfile(name) and not filecmp.cmp(filePath, name):
                # Check if file has been manually modified
                
                try:
                    if filePath in patchedFiles or not forceMerge:
                        if filePath.endswith(".txt") or filePath.endswith(".asset") or filePath.endswith(".gui"):
                            f = open(filePath,"r")
                            lines = f.readlines()
                            modification = lines[0]
                            f.close()
                            if "#MODIFIED" not in modification:
                                with open(filePath, "w") as dest:
                                    dest.write("#MODIFIED\n")
                                    dest.write("".join(lines))
                        file_path = Conflict(file_path,entry)
                    else:
                        os.remove(filePath)
    
                except Exception as e:
                    try :
                        file_path = Conflict(file_path,entry)
                    except Exception as e2:
                        print("/".join(file_path) + " Errored: " + str(e2))
            # Finalize our destination path
            filePath = os.sep.join(file_path)
            path = os.path.dirname(filePath)
            if not os.path.exists(path):
                os.makedirs(path)
            # Do not copy descriptor.mod, makes file explorer crash-y for some reason.
            if os.path.isfile(name) and ".mod" not in name and ".md" not in name:
                #print("moving " + name + " to " + filePath)
                copy2(name, filePath)
                if "mod/!conflicts!" not in filePath:
                    backup_path = file_path
                    backup_path[0] = "mod/! Modpack Baseline"
                    backupPath = filePath.replace("mod/! Modpack","mod/! Modpack Baseline")
                    #if not os.path.exists(backupPath):
                    #    os.makedirs(backupPath)
                    # copy2(name, backupPath)

    if not os.path.isfile("mod/Modpack.mod"):
        descriptor = open("mod/Modpack.mod","w+")
        descriptor.write("""name=\"! Modpack"
    path=\"mod/! Modpack\"
    tags={
        \"Gameplay\"
    }
    supported_version=\"3.*\"""")
    copy2("mod\\! Modpack\\", "mod\\Modpack baseline")
    print("Done!")

def Conflict(file_path,entry):
    fname, extension = file_path[-1].split('.')
    file_path[-1] = fname + "." +  extension + " " + entry.strip() + "." +  extension
    file_path[0] = "mod/!conflicts!"
    print_conflict_path = os.sep.join(file_path[1:])
    print(f"Confict detected. Moving to !conficts!{os.sep}{print_conflict_path}.")
    return file_path


if __name__ == "__main__":
    if os.path.isdir(f"mod{os.sep}!conflicts"):
        print("Resolve all conflicts and delete the conflicts folder before merging!")
        input()
    override = False
    while True:
        print("Force override files? (True/False) or (t/f) or (yes/no) or (y/n)")
        readin = input().lower()
        if readin in ['true', 'false', 't', 'f', 'yes', 'y', 'no', 'n']:
            if readin in ['true', 't', 'yes', 'y']:
                override = True
            break

    InitMerge(os.path.isdir(f"Pack Maker Utils{os.sep}! Modpack Baseline"),override)
    #make_modpack(modpack_name, overwrite)
   
