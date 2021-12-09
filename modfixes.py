import os
import glob
import re
from pathlib import Path

lgatePatch = False
targets = [
	# """is_machine_empire = yes""",
	# #"""has_ethic = ethic_gestalt_consciousness""",
	# """has_authority = auth_machine_intelligence""",
	# """authority = { value = auth_machine_intelligence }""",
	# """has_authority = \"auth_machine_intelligence\"""",
	# """has_ascension_perk = ap_synthetic_evolution"""
]
targets2 = {
	#r"power = \d*" : ["power = "]
	#r"_hull_add = \d*" : ["_hull_add = "],
	# r"_species_trait_points_add = \d" : ["_species_trait_points_add = "],
	# r"job_replicator_add = \d":["if = {limit = {has_authority = auth_machine_intelligence} job_replicator_add = ", "} if = {limit = {has_country_flag = synthetic_empire} job_roboticist_add = ","}"]
	}

targets3 = {

	#  "tile_resource_engineering_research_mult" : "planet_jobs_engineering_research_produces_mult",
	#  "tile_resource_physics_research_mult" : "planet_jobs_physics_research_produces_mult",
	#  "tile_resource_society_research_mult" : "planet_jobs_society_research_produces_mult",
	#  "pop_consumer_goods_mult" : "planet_pops_consumer_goods_upkeep_mult",
	#  "pop_food_req_mult" : "planet_pops_food_upkeep_mult",
	#  "tile_resource_energy_mult" : "planet_jobs_energy_produces_mult",
	#  "tile_resource_minerals_mult" : "planet_jobs_minerals_produces_mult",
	#  "tile_resource_food_mult" : "planet_jobs_food_produces_mult",
	#  "tile_resource_unity_mult" : "planet_jobs_unity_produces_mult",
	#  "pop_robot_build_speed_mult" : "pop_assembly_speed",
	#  "pop_robot_upkeep_mult" : "planet_pops_robotics_upkeep_mult",
	#  "pop_robot_build_cost_mult" : "planet_pop_assemblers_upkeep_mult",
	#  "country_resource_influence_add" : "country_base_influence_produces_add",
	#  "country_resource_unity_mult" : "country_base_unity_produces_mult",
	#  "pop_eff_wo_slaves" : "pop_cat_slave_happiness"

	# "has_starbase_size >= starbase_starfortress" : "has_starbase_size >= starbase_outpost"
	#"leader_trait = yes" : "leader_trait = { admiral }",
	#"trait_robot_domestic_protocols" : "trait_just-more-traits_robot_robosexuals"
	#"levels = 10" : "levels = 5"
	#"levels = -1" : "levels = 5"
	#"_species_trait_points_add = 1" : "_species_trait_points_add = 2"
	# "is_megastructure_type = lgate_base" : "OR = { is_megastructure_type = lgate_base is_megastructure_type = lgate_disabled}"
	#"has_ascension_perk = ap_machine_worlds has_ascension_perk = ap_synth_artificial_worlds" : "OR ={ has_ascension_perk = ap_machine_worlds has_ascension_perk = ap_synth_artificial_worlds }"
	# "default_robot" : "2dsynth_01",
	# "sd_mam_robot" : "mammaliansynth",
	# "sd_rep_robot" : "reptiliansynth",
	# "sd_avi_robot" : "aviansynth",
	# "sd_art_robot" : "arthropoidsynth",
	# "sd_mol_robot" : "synthetic_robot_01",
	# "sd_fun_robot" : "dragon_cyber2",
	# "sd_hum_robot" : "2dsynth_01",
	# "lith_machine" : "dragon_robot",
	#"has_ascension_perk = ap_synthetic_evolution" : "has_country_flag = synthetic_empire",
    #"create_built_robot_species" : "create_built_override_robot_species"
	
}

def replacer1(line):
	for target in targets:
		
		#has_ascension_perk = ap_synthetic_evolution 
		replacer = "OR = {has_country_flag = synthetic_empire "+target+"}"
		if target in line and replacer not in line: 
			#print(target)
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
	return line

def replacer2(line,i):
	for t,r in targets2.items():
		targets = re.findall(t,fileContents[i])
		if len(targets) > 0:
			for target in targets:
				
				value = int(target.split("=")[1])
				replacer = ""
				for j in range(len(r)):
					replacer += r[j]
					#if i < len(r) -1:
					replacer += str(int(value * 2))
				print(replacer)
				if target in line and replacer not in line: 
					line = line.replace(target,replacer)
	return line

def replacer3(line):
	for t,r in targets3.items():
		if t in fileContents[i]:
			line = line.replace(t,r)

	return line

fileList = glob.glob('mod/! Modpack/common/**',recursive=True)
#fileList = ["mod/! Modpack/common/component_templates/auxmodpack_cores.txt"]
#print(targets)
for _file in fileList: 
	if os.path.isfile(_file) and ".txt" in _file:
		
		fileContents = ""
		readFile = open(_file,"r")
		
		try:
			fileContents = readFile.readlines()
			text = "\n".join(fileContents)
			readFile.close()
			out = ""
			hasGate= False
			if lgatePatch:
			#print(text)
				if "is_megastructure_type = lgate_disabled" not in text:
					if "is_megastructure_type = lgate_base" in text:
						hasGate = True
			if not lgatePatch or hasGate:
				for i in range(0,len(fileContents)):
					line = fileContents[i]
					#out += replacer1(line)
					out += replacer3(line)
					#out += replacer2(line,i)
				#print(line)
				readFile = open(_file,"w")
				readFile.write(out)

		except Exception as e: 
			print(e)
			print("Unable to open",_file)
		readFile.close()
print("Done!")
input()

