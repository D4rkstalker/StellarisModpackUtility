import os
import glob
from pathlib import Path
from shutil import copy2
from whoosh.fields import Schema, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
import filecmp

modFiles = glob.glob('mod/ElvesofStellaris/**',recursive=True)
#allFiles = glob.glob('mod/**',recursive=True)
conflictingFiles = []
# schema = Schema(path=ID)
# if not os.path.exists("index"):
#     os.mkdir("index")
# ix = create_in("index", schema)
# ix = open_dir("index")

# def CreateIndex():
#     writer = ix.writer()

#     for _files in allFiles: 
#         if os.path.isfile(_files):
#             tempList = _files.split("\\")
#             del tempList[0]
#             del tempList[0]
#             _files = '/'.join(map(str, tempList))
#             #print("indexing: " + _files)
#             writer.add_document(path=_files)

#     writer.commit()
#CreateIndex()
#with ix.searcher() as searcher:
for _file in modFiles: 
    if os.path.isfile(_file):
        tempList = _file.split("\\")
        del tempList[0]
        files = '/'.join(map(str, tempList))
        # parser = QueryParser("path", ix.schema)
        # myquery = parser.parse(files)
        # results = searcher.search(myquery)
        print(files)
        # print(len(results))
        deleteDis = "mod/! Modpack/" + files
        try:
            if filecmp.cmp(deleteDis,_file): 
                if os.path.isfile(deleteDis):
                    print("deleting: " + deleteDis )
                    os.remove(deleteDis)
            else: 
                conflictingFiles.append(deleteDis)
        except: 
                print("Not found! : " + deleteDis)
for conflict in conflictingFiles:
    print ("conflicts: " + str(conflict))