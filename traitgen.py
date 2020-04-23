targets = ["physics_research","society_research","engineering_research","unity","alloys","minerals","energy","consumer_goods","food","volatile_motes","exotic_gases","rare_crystals"]
specialTargets = ["amenities","trade_value","defense_armies"]

template = """trait_priority_{} = {{
	cost = 0
	initial = yes
	randomized = no
	modification = yes
    ai_weight = {{ weight = 0 }}
	allowed_archetypes = {{ BIOLOGICAL ROBOT MACHINE LITHOID}}
}}
"""
n_template = """trait_negative_priority_{} = {{
	cost = 0
	initial = yes
	randomized = no
	modification = yes
    ai_weight = {{ weight = 0 }}
	allowed_archetypes = {{ BIOLOGICAL ROBOT MACHINE LITHOID}}
}}
"""

l_template = """ trait_priority_{}:0\"{} prioritization\"
 trait_priority_{}_desc:0\"Pops are more likely to take up jobs that produce {}\"\n"""
l_n_template = """ trait_negative_priority_{}:0\"{} avoidance\"
 trait_negative_priority_{}_desc:0\"Pops are less likely to take up jobs that produce {}\"\n"""

with open("traits.txt", 'w+') as f:
	for target in targets:
		f.write(template.format(target))		
		f.write(n_template.format(target))
	for target in specialTargets:
		f.write(template.format(target))		
		f.write(n_template.format(target))
with open("job_prio_traits.yml", 'w+') as f:
	f.write("l_english:\n")
	for target in targets:
		target1 = target.replace("_", " ")
		f.write(l_template.format(target,target1,target,target1))		
		f.write(l_n_template.format(target,target1,target,target1))
	for target in specialTargets:
		target1 = target.replace("_", " ")
		f.write(l_template.format(target,target1,target,target1))		
		f.write(l_n_template.format(target,target1,target,target1))
		