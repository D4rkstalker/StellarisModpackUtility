import glob
import os
import re

files = []
out_dir = ''

# slavery weight fix
weights_list = [
    '''
        modifier = {
            factor = 0.25
            is_enslaved = yes
            can_take_servant_job = no
            NOR = {
                has_trait = trait_nuumismatic_administration
                has_trait = trait_thrifty
            }
        }''',
    '''
        modifier = {
            factor = 2
            OR = {
                is_non_sapient_robot = yes
                is_shackled_robot = yes
            }
            can_take_servant_job = no
            owner = { has_technology = tech_droid_workers }
        }''',
    '''
        modifier = {
            factor = 200
            OR = {
                is_non_sapient_robot = yes
                is_shackled_robot = yes
            }
            can_take_servant_job = no
            owner = { NOT = { has_technology = tech_droid_workers } }
        }''',
    '''
        modifier = {
            factor = 10
            is_enslaved = yes
            can_take_servant_job = no
        }''',
    '''
        modifier = {
            factor = 2
            OR = {
                is_non_sapient_robot = yes
                is_shackled_robot = yes
            }
            can_take_servant_job = no
        }''',
    '''
        modifier = {
            factor = 0.25
            is_enslaved = yes
            can_take_servant_job = no
            NOR = {
                has_trait = trait_nuumismatic_administration
                has_trait = trait_thrifty
            }
        }''',
    '''
        modifier = {
            factor = 8
            is_enslaved = yes
            can_take_servant_job = no
            NOR = {
                has_trait = trait_syncretic_proles
                has_trait = trait_nuumismatic_administration
                has_trait = trait_robot_superconductive
                has_trait = trait_ingenious
            }
        }''',
]

slave_robot_weight = '''		modifier = {
            factor = 10
            OR = {
                is_enslaved = yes
                is_non_sapient_robot = yes
                is_shackled_robot = yes
            }
            can_take_servant_job = no
        }'''

buffer = 0


def jobs(files):
    for file in files:
        #print(file)
        out_file = os.path.join(out_dir, os.path.basename(file))
        with open(file, 'r') as f:
            text = f.read()

        text = re.sub('\t*\n', '\n', text)
        text = re.sub(' *\n', '\n', text)
        things = re.findall(r'\w*? = {.*?\n}', text, re.DOTALL)
        invalid_things = re.findall(r'#\w*? = {.*?\n}', text, re.DOTALL)
        with open(out_file, 'r') as f:
            for thing in things:
                try:
                    #Job selection fix 
                    lines = str(thing).split("\n")
                    for line in lines:
                        if "resources" in line and "{" in line:
                            buffer += 1
                                
                    print(lines[1])
                    #
                    #Job optimzation script stuff
                    
                    # skip = False
                    # for invalid in invalid_things:
                    #     if thing in invalid:
                    #         skip = True
                    # if skip:
                    #     f.write("#" + thing)
                    #     f.write('\n')
                    #     continue
                    # name = ''
                    # name = re.match(
                    #     r'[a-zA-Z]\w* = {', thing).group(0).replace(' = {', '').replace('\n', '')
                    # if 'is_capped_by_modifier = no' not in thing:
                    #     thing = thing.replace(
                    #         'possible = {',
                    #         'possible = {{\n\t\tor = {{\n\t\t\thas_job = {}\n\t\t\tz_pop_job_trigger = yes\n\t\t}}'.format(
                    #             name), 1)
                    #     if any(i in thing for i in weights_list):
                    #         for i in weights_list:
                    #             thing = thing.replace(i, '')

                    #         match = re.search('\n\tweight = {\n.*', thing)
                    #         if match:
                    #             weight = match.group(0)
                    #             thing = thing.replace(
                    #                 weight, weight + '\n' + slave_robot_weight)
                    # f.write(thing)
                    # f.write('\n')
                except Exception as e: 
                    print(e)


def parse_dir():
    global out_dir, files
    target_dir = "mod\\! Modpack\\common\\pop_jobs"
    out_dir = "mod\\! Modpack\\common\\pop_jobs"

    files += glob.glob(target_dir + '\\*.txt')


parse_dir()
jobs(files)
