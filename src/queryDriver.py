from utils import openOnePair
from simpleSearch import searchOnlyTerms
from phraseQuery import searchPhrase
import json
import pickle
import time
import os
"""
sampleInput = {
                    "query":
                    {
                        "mode":0,
                        "fileName" : "BBCNEWS.201701",
                        "search" : ["got" , "getting"],
                        "top":3
                    }
                }
"""
# search: this is my name 
sampleInput = {
                  "query":
                    {
                        "mode":1,
                        "fileName" : "BBCNEWS.201701",
                        "must" : "nino weather" ,
                        "top":8
                    } 
                }
def simpleSearchOnOneFile(sampleInput):

    fileName = sampleInput["query"]["fileName"]
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = [searchTerm.lower() for searchTerm in sampleInput["query"]["search"]]

    start = time.time()

    result = searchOnlyTerms(searchTerms, invertedIndex, topK, max([int(x) for x in docInfo]))

    end = time.time()

    finalRes = {}
    for i in range(len(result)):
        finalRes[result[i][0]] = {"score":result[i][1],"document":docInfo[str(result[i][0])]}
                        

    print(json.dumps(finalRes,indent=1))
    print(f"operation took: {end - start}")



def simpleSearchOnAllFiles(sampleInput):

    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = [searchTerm.lower() for searchTerm in sampleInput["query"]["search"]]
    allIndexes = os.listdir("../indexes/")
    allDocumentsInfo = os.listdir("../documentInfo")
    jsonPrefix = "../documentInfo/"
    picklePrefix = "../indexes/"
    finalRes = {}

    start = time.time()

    for i in range(417):

        filePrefix = allDocumentsInfo[i][:-5]
        with open(jsonPrefix+filePrefix+".json", 'r') as f:
            docInfo = json.load(f)


        with open(picklePrefix+filePrefix+".pickle", 'rb') as file:
            invertedIndex = pickle.load(file)

        result = searchPhrase(searchTerms, invertedIndex, topK)

        for res in range(len(result)):
            finalRes[filePrefix + "_" +str(result[res][0])] = {"score":result[res][1],"document":docInfo[str(result[res][0])]}

    end = time.time()
    for top in sorted(finalRes, key=lambda x: finalRes[x]["score"], reverse=1)[:topK]:
        print(json.dumps({top:finalRes[top]}, indent=1))
        
    print(f"operation took: {end - start}")

def simplePhraseOnOneFile(sampleInput):
    fileName = sampleInput["query"]["fileName"]
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = sampleInput["query"]["must"]

    docInfo , invertedIndex = openOnePair(fileName)
    start = time.time()

    result = searchPhrase(searchTerms, invertedIndex, topK)

    finalRes = {}
    end = time.time()
    for i in range(len(result)):
        finalRes[result[i][0]] = {"score":result[i][1],"document":docInfo[str(result[i][0])]}
                        
    print(json.dumps(finalRes,indent=1))
    print(f"operation took: {end - start}")

def simplePhraseOnAllFiles(sampleInput):
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = sampleInput["query"]["must"]
    allIndexes = os.listdir("../indexes/")
    allDocumentsInfo = os.listdir("../documentInfo")
    jsonPrefix = "../documentInfo/"
    picklePrefix = "../indexes/"
    finalRes = {}

    start = time.time()
    
    for i in range(417):

        filePrefix = allDocumentsInfo[i][:-5]
        with open(jsonPrefix+filePrefix+".json", 'r') as f:
            docInfo = json.load(f)


        with open(picklePrefix+filePrefix+".pickle", 'rb') as file:
            invertedIndex = pickle.load(file)

        result = searchPhrase(searchTerms, invertedIndex, topK)

        for res in range(len(result)):
            finalRes[filePrefix + "_" +str(result[res][0])] = {"score":result[res][1],"document":docInfo[str(result[res][0])]}

    end = time.time()
    for top in sorted(finalRes, key=lambda x: finalRes[x]["score"], reverse=1)[:topK]:
        print(json.dumps({top:finalRes[top]}, indent=1))
        
    print(f"operation took: {end - start}")



if(sampleInput["query"]["mode"]):
    if("search" in sampleInput["query"]):
        simpleSearchOnAllFiles(sampleInput)
    elif("must" in sampleInput["query"]):
        simplePhraseOnAllFiles(sampleInput)
else:
    if("search" in sampleInput["query"]):
        simpleSearchOnOneFile(sampleInput)
    elif("must" in sampleInput["query"]):
        simplePhraseOnOneFile(sampleInput)