import glob
import os
import re
import collections
import json
import operator
import copy
from recordtype import recordtype
files = []
invalids = {' ':'STL2PY_REPLACE_SPACE_',
            '<' : 'STL2PY_REPLACE_LESS_',
            '>' : 'STL2PY_REPLACE_MORE_',
            '@' : 'STL2PY_REPLACE_AT_',
            ':' : 'STL2PY_REPLACE_COLON_'
            }

def Convert():
    for file in files:
        #print("converting")
        f =  open(file, 'r',encoding="utf-8")
        _file = f.read()
        f.close()
        text = []
        _file = re.sub('\t*\n', '\n', _file)
        _file = re.sub(' *\n', '\n', _file)
        _file = re.sub('{','{\n',_file)
        _file = re.sub('}','\n}',_file)
        _file = re.sub('\"','',_file)

        # Remove Comments
        for line in _file.split("\n"):
            if "#" in line:
                line = line.split("#")[0]
            text.append(line + "\n")
        # Format Input
        #print(text)
        out = "{"
        layer = 0
        for line in text:
            if "{" in line:
                layer +=1
                #print(line)
                temp = line.split("=")
                out += "\"{}\"".format(Replacer(temp[0])) + ": {"
                #print(temp)
            elif "}" in line:
                layer -=1
                out += "},"
            elif "=" in line:
                temp = line.split("=")
                out += "\"{}\" : \"{}\",".format(Replacer(temp[0]),Replacer(temp[1]))
            elif not line.isspace():
                #print(line)
                out += "\"KEY_LESS_VALUE\":\"{}\",".format(line)
        out = out + "}"

        out = re.sub('\n','',out)
        out = re.sub('\t','',out)
        out = re.sub(',}','}',out)
        
        #out = re.sub(' ','STL2PY_REPLACE_SPACE_',out)
        
        #print(out)
        try:
            x = json.loads(out, object_hook=lambda d: recordtype('X', d.keys())(*d.values()))
        except Exception as e:
            print("\n-----")
            print(e)
            print(out)
            print(file)
        #print(UnMap(str(x)))

def Replacer(str_in):
    for key in invalids:
        str_in = re.sub(key,invalids[key],str_in)
    return "STL2PY_REPLACE_START" + str_in

def UnMap(str_in):
    str_in = re.sub('STL2PY_REPLACE_START','',str_in)
    for key in invalids:
        str_in = re.sub(invalids[key],key,str_in)
    return str_in







def parse_dir():
    global files
    target_dir = "mod\! Modpack\common\solar_system_initializers"

    files += glob.glob(target_dir + '\\*.txt')



parse_dir()
Convert()