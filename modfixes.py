import os
import glob
import re
from pathlib import Path

targets = [
	# """is_machine_empire = yes""",
	# #"""has_ethic = ethic_gestalt_consciousness""",
	# """has_authority = auth_machine_intelligence""",
	# """authority = { value = auth_machine_intelligence }""",
	# """has_authority = \"auth_machine_intelligence\"""",
	# """has_ascension_perk = ap_synthetic_evolution"""
]
targets2 = {
	# r"MACHINE_species_trait_points_add = \d" : ["MACHINE_species_trait_points_add ="," ROBOT_species_trait_points_add = ",""],
	# r"job_replicator_add = \d":["if = {limit = {has_authority = auth_machine_intelligence} job_replicator_add = ", "} if = {limit = {has_country_flag = synthetic_empire} job_roboticist_add = ","}"]
	}

targets3 = {
	#"has_country_flag = synthetic_empire" : "has_ascension_perk = ap_synthetic_evolution"
	# "tile_resource_engineering_research_mult" : "planet_jobs_engineering_research_produces_mult",
	# "tile_resource_physics_research_mult" : "planet_jobs_physics_research_produces_mult",
	# "tile_resource_society_research_mult" : "planet_jobs_society_research_produces_mult",
	# "pop_consumer_goods_mult" : "planet_pops_consumer_goods_upkeep_mult",
	# "pop_food_req_mult" : "planet_pops_food_upkeep_mult",
	# "tile_resource_energy_mult" : "planet_jobs_energy_produces_mult",
	# "tile_resource_minerals_mult" : "planet_jobs_minerals_produces_mult",
	# "tile_resource_food_mult" : "planet_jobs_food_produces_mult",
	# "tile_resource_unity_mult" : "planet_jobs_unity_produces_mult",
	# "pop_robot_build_speed_mult" : "pop_assembly_speed",
	# #"leader_trait = yes" : "leader_trait = { admiral }"
	# "pop_robot_upkeep_mult" : "planet_pops_robotics_upkeep_mult",
	# "pop_robot_build_cost_mult" : "planet_pop_assemblers_upkeep_mult",
	# "country_resource_influence_add" : "country_base_influence_produces_add",
	# "country_resource_unity_mult" : "country_base_unity_produces_mult",
	# "pop_eff_wo_slaves" : "pop_cat_slave_happiness"
	#"trait_robot_domestic_protocols" : "trait_just-more-traits_robot_robosexuals"
	"levels = -1" : "levels = 5"
	#"has_ascension_perk = ap_machine_worlds has_ascension_perk = ap_synth_artificial_worlds" : "OR ={ has_ascension_perk = ap_machine_worlds has_ascension_perk = ap_synth_artificial_worlds }"
}
	
fileList = glob.glob('mod/! Modpack/common/technology/**',recursive=True)
print(targets)
for _file in fileList: 
	if os.path.isfile(_file) and ".txt" in _file:
		print(_file)
		fileContents = ""
		readFile = open(_file,"r")
		try:
			fileContents = readFile.readlines()
			readFile.close()
			out = ""
			for i in range(0,len(fileContents)):
				line = fileContents[i]
				#print(line)
				# for target in targets:
					
				# 	#has_ascension_perk = ap_synthetic_evolution 
				# 	replacer = "OR = {has_country_flag = synthetic_empire "+target+"}"
				# 	if target in line and replacer not in line: 
				# 		#print(target)
				# 		shouldReplace = True
				# 		for j in range(i,0,-1):
				# 			if "{" in fileContents[j]:
				# 				if "NOR" in fileContents[j] or "NOT" in fileContents[j] :
				# 					shouldReplace = False
				# 				#print (fileContents[j])
				# 				break
				# 		#print(line)
				# 		if shouldReplace:
				# 			line = line.replace(target,replacer)
				# for t,r in targets2.items():
				# 	targets = re.findall(t,fileContents[i])
				# 	if len(targets) > 0:
				# 		for target in targets:

				# 			value = target.split("=")[1]
				# 			replacer = ""
				# 			for i in range(len(r)):
				# 				replacer += r[i]
				# 				if i < len(r) -1:
				# 					replacer += value
				# 			if target in line and replacer not in line: 
				# 				line = line.replace(target,replacer)
				for t,r in targets3.items():
					if t in fileContents[i]:
						line = line.replace(t,r)
							


				out += line
			readFile = open(_file,"w")
			readFile.write(out)

		except Exception as e: 
			print(e)
			print("Unable to open",_file)
		readFile.close()
print("Done!")
input()

