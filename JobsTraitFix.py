import glob
import os
import re

print("Modname:")
JOBS_FOLDER = "mod\\" + input() + "\\common\\pop_jobs"

files = []

template = """\n	triggered_planet_modifier = {{
		potential = {{
			has_trait = {}
		}}
		modifier = {{
			{} = {}
		}}
	}}
"""


def jobs(files):
    for file in files:
        #print(file)
        out_file = os.path.join(out_dir, os.path.basename(file))
        with open(file, 'r') as f:
            text = f.read()
        if "trait_just-more-traits_robot_robosexuals" not in text:

            text = re.sub('\t*\n', '\n', text)
            text = re.sub(' *\n', '\n', text)
            jobs = re.findall(r'\w*? = {.*?\n}', text, re.DOTALL)
            with open(out_file, 'w') as f:
                for job in jobs:
                    #f.write("#PATCHED: Job traits\n")
                    #try:
                        #Job selection fix 
                    lines = str(job).split("\n")
                    layers = 0
                    trigger = False
                    modifier = False
                    trade_added = False
                    for line in lines:
                        if "{" in line:
                            #print(nextLine + "+")
                            layers +=1
                        if "}" in line:
                            layers -=1
                        #print(line + str(layers))

                        if layers == 1:
                            
                            trigger = False
                            #print(nextLine + "-")
                        if "triggered_planet_modifier" in line:
                            print(line + str(layers))
                            trigger = True
                        if trigger and ("trait_robot_domestic_protocols" in line or "trait_charismatic" in line):
                            modifier = True                                            
                        f.write(line)
                        if layers == 1 and modifier and template.format("trait_just-more-traits_robot_robosexuals","planet_amenities_add","6.9") not in job:
                            f.write(template.format("trait_just-more-traits_robot_robosexuals","planet_amenities_add","6.9"))
                        if layers == 1 and "trade_value_add" in job and not trade_added and template.format("trait_just-more-traits_robot_robosexuals","trade_value_add","6.9") not in job:
                            f.write(template.format("trait_just-more-traits_robot_robosexuals","trade_value_add","6.9"))
                            trade_added = True
                        if layers ==1:
                            modifier = False

                        f.write("\n")
                        
                    # except Exception as e: 
                    #     print(e)
        else:
            print("patch already applied to " + file + "!, skipping")
                

def parse_dir():
    global out_dir, files
    target_dir = JOBS_FOLDER
    out_dir = JOBS_FOLDER

    files += glob.glob(target_dir + '\\*.txt')


parse_dir()
jobs(files)
print("done!")
input()
