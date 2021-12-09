import os
import glob
import json
from shutil import copy2
from filecmp import cmp as compare
from argparse import ArgumentParser
from make_mod_patch import mod_patch


def make_modpack(modpack_name, overwrite):
    print("\nAssembling modpack...")
    fileIndex = dict()
    whitelist = open('whitelist.txt').read().split('\n')
    # Keep only the alphanumeric characters in the names in the whitelist, remove blank lines:
    whitelist = [''.join(char for char in list_entry if char.isalnum()) for list_entry in whitelist if list_entry]

    patch_created = False
    if os.path.isdir(f"mod{os.sep}{modpack_name}") and not overwrite:
        print(f"The {modpack_name} directory already exists...")
        patch_name = ''.join(char for char in modpack_name if char.isalnum()) + "Patch"
        if os.path.isdir(f"mod{os.sep}{patch_name}"):
            print("It looks like a modpack patch has already been created for this modpack. Checking for new changes.")
            new_changes_present = mod_patch(modpack_name, check_only=True)
            if new_changes_present:
                print(f"\nIt looks like there are additional changes in your {modpack_name} folder aside from those saved in {patch_name}.")
                print(f"This process will abort in order to prevent loss of changes in your {modpack_name} or overwriting of files in your {patch_name} folder.")
                print(f"To force skip the patch creation process and overwrite files in the {modpack_name} folder, run \"installer.py -ovr\"")
                print(f"To force the updating of the contents of {patch_name}, run \"make_mod_patch.py\" and then run \"installer.py\" again.")
                print("If the only differing files are in the modpack patch itself, you must run \"installer.py -ovr\" to push those files into the modpack.")
                return
            else:
                print("There are no additional changes in the modpack aside from those already in the patch.")
        else:
            patch_created = mod_patch(modpack_name, add_to_whitelist=False)
        print("Continuing to assemble modpack...\n")

    for entry in whitelist:
        fileList = glob.glob(f'mod{os.sep}{entry}{os.sep}interface{os.sep}**', recursive=True)
        for cur_file in fileList:
            if not os.path.isfile(cur_file) or ".mod" in cur_file:
                continue  # Skip directory the folders themselves and mod descriptor files.
            file_path = cur_file.split(os.sep)
            file_path[1] = modpack_name  # Change folder to the modpack.
            path_within_mod = os.sep.join(file_path[2:])
            if path_within_mod in fileIndex:
                # There is already a file at this path in the modpack, it is either a conflict or a duplicate.
                if compare(cur_file, os.sep.join(file_path)):
                    fileIndex[path_within_mod][0].append(f"DUPLICATE: {entry.strip()}")
                    fileIndex[path_within_mod][2] += 1
                    continue  # Skip duplicate files.
                # File is a conflict:
                fileIndex[path_within_mod][0].append(f"CONFLICT: {entry.strip()}")
                fileIndex[path_within_mod][1] += 1
                file_path[1] = f"{modpack_name}_conflicts!"  # Copy the conflicting file to the conflicts folder.
                fname, extension = file_path[-1].split('.')
                file_path[-1] = fname + "." + extension + " " + entry.strip() + "." +  extension
                print(f"Confict detected. Moving to {os.sep.join(file_path[1:])}.")
            else:
                # First time we've seen a file at this path.
                # First entry in the dict is for mod source, second is for conflict count, third is for repeat count.
                fileIndex[path_within_mod] = [[(f"SELECTED: {entry.strip()}")], 0, 0]
            # Make dirs if necessary:
            target_path = os.sep.join(file_path)
            target_dir = os.path.dirname(target_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            # Copy the mod file to its destination.
            copy2(cur_file, target_path)

    print("\n\nDone copying files.")
    if fileIndex:
        with open(f'mod{os.sep}{modpack_name}{os.sep}whitelist.txt', "w+") as f:
            f.writelines([i +'\n' for i in whitelist])

        conflicts_dict = dict()
        duplicates_dict = dict()
        for i in fileIndex:
            if fileIndex[i][1]:
                conflicts_dict[i] = fileIndex[i][0]
            if fileIndex[i][2]:
                duplicates_dict[i] = fileIndex[i][0]
            fileIndex[i] = fileIndex[i][0]

        # Output a list of all files.
        with open(f"mod{os.sep}{modpack_name}{os.sep}allFilesList.txt", "w+") as f:
            f.write(json.dumps(fileIndex, indent = 4))
        if duplicates_dict:
            # Output a list of duplicate files.
            with open(f"mod{os.sep}{modpack_name}{os.sep}duplicateFilesList.txt", "w+") as f:
                f.write(json.dumps(duplicates_dict, indent = 4))
            print(f"Duplicate files listed in mod{os.sep}{modpack_name}{os.sep}duplicateFilesList.txt")
        if conflicts_dict:
            # Output a list of conflicting files.
            with open(f"mod{os.sep}{modpack_name}_conflicts!{os.sep}conflictingFilesList.txt", "w+") as f:
                f.write(json.dumps(conflicts_dict, indent = 4))
            print(f"Conflicting files listed in mod{os.sep}{modpack_name}_conflicts!{os.sep}conflictingFilesList.txt")
        else:
            print("No conflicts!")

    mod_descriptor_name = ''.join(char for char in modpack_name if char.isalnum()).capitalize()
    if not os.path.isfile(f"mod{os.sep}{mod_descriptor_name}.mod"):
        with open(f"mod{os.sep}{mod_descriptor_name}.mod", "w+") as f:
            f.writelines([f"name=\"{modpack_name}\"\n", f"path=\"mod/{modpack_name}\"\n", "tags={\n", "\t\"Gameplay\"\n", "}\n", "supported_version=\"2.7.*\"\n"])

    if patch_created:
        print("A modpack patch was created in order to preserve the customizations in the modpack folder.")
        print(f"To revert the customizations to your modpack, add {patch_name} to your whitelist (at the top if you want to ensure your customizations are prioritized).")
    print("Done!")


def get_name_from_cl():
    parser = ArgumentParser()
    parser.add_argument('-n', '--modpack_name', default="! modpack", type=str,
        help='The name of the modpack (both the folder name and the name in the stellaris launcher).')
    parser.add_argument('-ovr', '--nopatch', action='store_true', default=True,
        help="Add this argument to overwrite files in the mod folder without generating a patch. By default, " \
            "modifications within the *modpack_name* folder will be saved to a new mod called *modpack_name*_patch")
    args = parser.parse_args()
    return args.modpack_name, args.nopatch


if __name__ == "__main__":
    modpack_name, overwrite = get_name_from_cl()
    print(overwrite)
    make_modpack(modpack_name, overwrite)
