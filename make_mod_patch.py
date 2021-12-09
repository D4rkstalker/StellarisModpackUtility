# This utility examines all the files in the ! Modpack folder (or in the folder specified by the -mod command line argument).
# The files are compared to the files in the extracted mod folders that would be put into the modpack folder according to the whitelist.txt file.
# Any files in the modpack folder that differ from the expected file are copied into the mod\ModpackPatch folder.

# What is the point of all this?

# After merging mods into a modpack, a user may want to replace one of the conflicting files with a file from a different mod,
# or perhaps even make manual modifications to the files in the modpack.
# Running this script to create a modpack patch is a way to sort of "save" the changes made to a modpack.

# The various mods in the modpack can then be updated via the standard workflow when new releases of any of the mods come out,
# after which a user can compare changed files in the mod with their custom changes in the patch through whatever diff method the user prefers.

# The modpackPatch is not intended to be added to your active mods in the stellaris launcher (it will add nothing the modpack doesn't already add)
# it's just a tool to help customize modpacks, save modified files, and save the way you've resolved conflicts,
# and then easily re-impliment or diff the changes you've made when new versions of the mods come out or when you add new mods to the modpack.

import os
import glob
from os.path import isfile

from shutil import copy2
from filecmp import cmp as compare
from argparse import ArgumentParser


def mod_patch(modpack_name, add_to_whitelist=True, check_only=False):
    changes_present = False
    changeSet = set()
    patch_name = modpack_name + "Patch"
    print(f"\nChecking for customizations in {modpack_name}...\n")
    fileSet = {"duplicateFilesList.txt", "allFilesList.txt", "whitelist.txt"}  # To avoid copying these meta lists to the patch folder.
    patch_created = False
    # Keep only the alphanumeric characters in the names in the whitelist, remove blank lines:
    fileList = glob.glob('mod\\! Modpack Baseline\\**', recursive=True)
    for cur_file in fileList:
        if not os.path.isfile(cur_file) or ".mod" in cur_file:
            continue  # Skip directory the folders themselves and mod descriptor files.
        file_path = cur_file.split(os.sep)
        file_path[0] = "mod"  # Change folder to the modpack.
        file_path[1] = modpack_name  # Change folder to the modpack.
        path_within_mod = os.sep.join(file_path[2:])
        if path_within_mod in fileSet:
            # A file with this path has already been compared.
            # The cur_file might be a conflict or maybe a duplicate.
            # Either way, no checking is necessary, so go to the next file.
            continue
        try:
            if not isfile(os.sep.join(file_path)):
                with open(os.sep.join(file_path),"w+") as f:
                    f.write("#Overriden")
            #print(cur_file)
            #print(file_path)
            if compare(cur_file, os.sep.join(file_path)):
                # The first mod on the whitelist that has this file has an identical file to the file in the modpack.
                # This means no customization has been made, and nothing need be done.
                fileSet.add(path_within_mod)
            else:
                # This file has been altered.
                if check_only:
                    changes_present = True
                    if path_within_mod not in changeSet:
                        print(f"File in modpack differs from file in mod: {os.sep.join(cur_file.split(os.sep)[1:])}")
                    changeSet.add(path_within_mod)
                    continue  # Advance to next file without any copying.
                # Copy the file to the patch folder.
                print(f"Adding customized file to patch: {path_within_mod}")
                patch_created = True
                fileSet.add(path_within_mod)
                modified_file = os.sep.join(file_path)
                file_path[1] = patch_name  # Change folder to the patch.
                target_path = os.sep.join(file_path)
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                copy2(modified_file, target_path)
        except Exception as e:
            print(cur_file)
            print(e)
            print(f"Adding customized file to patch: {path_within_mod}")
            patch_created = True
            fileSet.add(path_within_mod)
            modified_file = os.sep.join(file_path)
            file_path[1] = patch_name  # Change folder to the patch.
            target_path = os.sep.join(file_path)
            target_dir = os.path.dirname(target_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            copy2(modified_file, target_path)

    # Check the modpack for unique files that are not present in any of the mods on the whitelist.
    all_mod_files = glob.glob(f'mod{os.sep}{modpack_name}{os.sep}**', recursive=True)
    for cur_file in all_mod_files:
        if not os.path.isfile(cur_file) or ".mod" in cur_file:
            continue  # Skip directory the folders themselves and mod descriptor files.
        file_path = cur_file.split(os.sep)
        path_within_mod = os.sep.join(file_path[2:])
        if path_within_mod not in fileSet:
            # Even after looking through all of the mods, we've never seen this file. It must be new.
            if check_only:
                changes_present = True
                if path_within_mod not in changeSet:
                    print(f"File has been added to modpack: {path_within_mod}")
                changeSet.add(path_within_mod)
                continue  # Advance to next file without any copying.
            # Copy the new file to the patch.
            print(f"Adding unique file to patch: {path_within_mod}")
            patch_created = True
            file_path = cur_file.split(os.sep)
            file_path[1] = patch_name
            target_path = os.sep.join(file_path)
            target_dir = os.path.dirname(target_path)
            if not os.path.exists(target_dir):
                 os.makedirs(target_dir)
            copy2(cur_file, target_path)

    if check_only:
        if changes_present:
            return True
        return False  # Done checking for new changes - there were none!

    if patch_created:
        if not os.path.isfile(f"mod{os.sep}{patch_name}.mod"):
            with open(f"mod{os.sep}{patch_name}.mod", "w+") as f:
                f.writelines([f"name=\"{patch_name}\"\n", f"path=\"mod{os.sep}{patch_name}\"\n", "tags={\n", "\t\"Gameplay\"\n", "}\n", "supported_version=\"3.*.*\"\n"])
        print(f"\n\nCustomized files in \"{modpack_name}\" have been copied to \"{patch_name}\".{' The patch has been added to your whitelist.' if add_to_whitelist else ''}\n")
    else:
        print(f"\n\nNo customized files found in \"{modpack_name}\". No patch created.\n")

    # Return a bool indicating that a patch has indeed been created.
    return patch_created


def get_name_from_cl():
    parser = ArgumentParser()
    parser.add_argument('-n', '--modpack_name', default="! modpack", type=str,
        help='The name of the modpack (both the folder name and the name in the stellaris launcher).')
    args = parser.parse_args()
    return args.modpack_name


if __name__ == "__main__":
    modpack_name = get_name_from_cl()
    mod_patch(modpack_name)
