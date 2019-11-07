import os
import glob
import re
from pathlib import Path

targets = [
	"""is_machine_empire = yes""",
	"""has_ethic = ethic_gestalt_consciousness""",
	"""has_authority = auth_machine_intelligence""",
	"""authority = { value = auth_machine_intelligence }""",
	"""has_authority = \"auth_machine_intelligence\"""",
	"""has_ascension_perk = ap_synthetic_evolution""",
]
targets2 = {
	r"MACHINE_species_trait_points_add = \d" : ["MACHINE_species_trait_points_add ="," ROBOT_species_trait_points_add = ",""],
	r"job_replicator_add = \d":["if = {limit = {has_authority = auth_machine_intelligence} job_replicator_add = ", "} if = {limit = {has_country_flag = synthetic_empire} job_roboticist_add = ","}"]
	}

targets3 = {
	"has_country_flag = synthetic_empire" : "has_ascension_perk = ap_synthetic_evolution"
}
	
fileList = glob.glob('mod/! Modpack/**',recursive=True)
#print(targets2)
for _file in fileList: 
	if os.path.isfile(_file) and ".txt" in _file:
		#print(_file)
		fileContents = ""
		readFile = open(_file,"r")
		try:
			fileContents = readFile.readlines()
			readFile.close()
			out = ""
			for i in range(0,len(fileContents)):
				line = fileContents[i]
				for target in targets:
					#has_ascension_perk = ap_synthetic_evolution 
					replacer = "OR = {has_ascension_perk = ap_synthetic_evolution "+target+"}"
					if target in line and replacer not in line: 
						shouldReplace = True
						for j in range(i,0,-1):
							if "{" in fileContents[j]:
								if "NOR" in fileContents[j] or "NOT" in fileContents[j] :
									shouldReplace = False
								#print (fileContents[j])
								break
						#print(line)
						if shouldReplace:
							line = line.replace(target,replacer)
				for t,r in targets2.items():
					targets = re.findall(t,fileContents[i])
					if len(targets) > 0:
						for target in targets:

							value = target.split("=")[1]
							replacer = ""
							for i in range(len(r)):
								replacer += r[i]
								if i < len(r) -1:
									replacer += value
							if target in line and replacer not in line: 
								line = line.replace(target,replacer)
				for t,r in targets3.items():
					if t in fileContents[i]:
						line = line.replace(t,r)
							


				out += line
		except Exception as e: 
			print(e)
			print("Unable to open",_file)
		readFile = open(_file,"w")
		readFile.write(out)
		readFile.close()

