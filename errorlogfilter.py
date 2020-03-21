log = open("logs/error.log",encoding="utf8")
filters = [
    """[persistent.cpp:33]""", #Unexpected token errors
]
logs = log.readlines()

with open("filteredLog.txt","w+") as out:
    for i in range(len(logs)):
        line = logs[i]
        for _filter in filters:
            if _filter in line:
                try:
                    out.write(line)
                    if _filter == "[persistent.cpp:33]":
                        out.write(logs[i+1])
                except:
                    pass
                break           
