Requirements:

-Python 3.6

-7z (Add the 7z folder to your windows enviroment path variable. File explorer crashes when extracting the descriptor.mod)

Usage: 

-Place all scripts in C:\Users\<your username>\Documents\Paradox Interactive\Stellaris\

-Edit generateModList.py and extractor.py, change STEAM_PATH to your steam installation directory

-Run generateModList.py 

  >Mods which are not updated for 2.4+ will be listed according to their zip file name, which may be abbreviated
  
-Copy the mods that you want to merge from list.txt to whitelist.txt

-Run extractor.py 

-Run installer.py

-Output is in mod/! Modpack/

-Conflicts are in mod/!conflicts!/

-Merge the conflicting files 

  >Notepad++ w/ the compare plugin probably the quickest and simplest, although it does occasionaly get confused with the more complex files



GenerateModList.py: 

-Generates a list of installed mods 

-outputs to list.txt 


Extractor.py:

-Reads from whitelist.txt 

-Extracts/Copies files from the steamworkshop folder into the local mod folder 


Installer.py: 

-Reads from whitelist.txt 

-Copies mods into /Mod/! Modpack/ 

-Conflicts are copied into /!Conflicts!/ as <Filename> + <Modname>
  
-Will skip files that have the same contents compared to the files already present in /! Modpack/

-Generated a list of copied files under /mod/!conflicts!/filesList.txt, useful for determining which file to overwrite
  
  
Uninstaller.py:

-Remove all files from the selected mod

-Prints conflicts to the console


Modfixes.py: 

-Used to make batch changes to mods 


SetUpMods.py: 

-Generates descriptor.mod for extracted mods
