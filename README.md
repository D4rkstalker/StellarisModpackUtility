# Requirements

-Python 3.6

-Add the 7z folder to your windows enviroment path (File explorer crashes when extracting the descriptor.mod, so i used 7z instead)

> In Search, search for and then select: System (Control Panel)

> Click the Advanced system settings link.

> Click Environment Variables. In the section System Variables, find the PATH environment variable and select it. Click Edit. If the PATH environment variable does not exist, click New.

> In the Edit System Variable (or New System Variable) window, click new and add the 7z installation directory. Click OK. Close all remaining windows by clicking OK.

> Reopen any command prompt windows.

# Usage

-Place all scripts in C:\Users\<your username>\Documents\Paradox Interactive\Stellaris\

-Run generateModList.py

>This will create list.txt which contains a list of all installed mods and an empty whitelist.txt 

>Mods which are not updated for 2.4+ will be listed according to their zip file name, which may be abbreviated
  

-Copy the mods that you want to merge from list.txt to whitelist.txt

-Run extractor.py

> This will extract all whitelisted mods into your local mod folder

> Depending on the mods, this may use up several GB's worth of space

-Run installer.py

> The merged pack is in mod/! Modpack/

> Conflicts are in mod/!conflicts!/

-Merge the conflicting files

> Notepad++ w/ the compare plugin is probably the quickest and simplest, although it does occasionaly get confused with the more complex files

# Other scripts

OrbitalDepositsBoost.py:

-Increases orbital deposits

systemInitializerMod.py:

-Force all unique systems to spawn

Uninstaller.py:

-Remove all non modified files of a selected mod from the modpack

> Edit the script and change the mod name to the mod to be removed

-Prints conflicts to the console

Modfixes.py:

-Used to make batch changes to mods

SetUpMods.py:

-Generates descriptor.mod for extracted mods

localisator.py:

-Generates and updates localisation keys from English to other languages