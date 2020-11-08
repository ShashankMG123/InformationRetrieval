from utils import openOnePair, openBigram, compareOutputs
from simpleSearch import searchOnlyTerms
from phraseQuery import searchPhrase
from wildcardQuery import wildCardQuery
from compareES import queryES
import json
import pickle
import time
import os


COMPARE_MODE = 1


sampleInput = {
                    "query":
                    {
                        "mode":1,
                        "fileName" : "CNN.200909",
                        "search" : ["chirp","gas"],
                        "top":10
                    }
                }




# sampleInput = {
#                   "query":
#                     {
#                         "mode":0,
#                         "fileName" : "CNN.200909",
#                         "wildcard" : "ca*" ,
#                         "top":10
#                     } 
#                 }


# search: this is my name 

# sampleInput = {
#                   "query":
#                     {
#                         "mode":0,
#                         "fileName" : "BBCNEWS.201701",
#                         "must" : "naskjfdbaofbaisobf" ,
#                         "top":8
#                     } 
#                 }

def simpleSearchOnOneFile(sampleInput):

    fileName = sampleInput["query"]["fileName"]
    docInfo , invertedIndex = openOnePair(fileName)
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = [searchTerm.lower() for searchTerm in sampleInput["query"]["search"]]

    start = time.time()

    result = searchOnlyTerms(searchTerms, invertedIndex, topK, max([int(x) for x in docInfo]))

    end = time.time()

    finalRes = {}
    for i in range(len(result)):
        finalRes[result[i][0]] = {"score":result[i][1],"document":docInfo[str(result[i][0])]}
                        
    return(finalRes, (end - start))
    



def simpleSearchOnAllFiles(sampleInput):

    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = [searchTerm.lower() for searchTerm in sampleInput["query"]["search"]]
    allIndexes = os.listdir("..\\indexes\\")
    allDocumentsInfo = os.listdir("..\\documentInfo\\")
    jsonPrefix = "..\\documentInfo\\"
    picklePrefix = "..\\indexes\\"
    finalRes = {}

    start = time.time()

    for i in range(417):

        filePrefix = allDocumentsInfo[i][:-5]
        
        with open(jsonPrefix+filePrefix+".json", 'r') as f:
            docInfo = json.load(f)


        with open(picklePrefix+filePrefix+".pickle", 'rb') as file:
            invertedIndex = pickle.load(file)

        result = searchOnlyTerms(searchTerms, invertedIndex, topK , max([int(x) for x in docInfo]))
        # print(result)
        for res in range(len(result)):
            finalRes[result[res][0]] = {"score":result[res][1],"document":docInfo[str(result[res][0])]}

    end = time.time()

    FinalRes = dict()

    if(finalRes):
        for top in sorted(finalRes, key=lambda x: finalRes[x]["score"], reverse=1)[:topK]:
            print(json.dumps({top:finalRes[top]},indent=1))
            FinalRes[top] = finalRes[top]

    return (FinalRes,(end - start))

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
    allIndexes = os.listdir("..\\indexes\\")
    allDocumentsInfo = os.listdir("..\\documentInfo\\")
    jsonPrefix = "..\\documentInfo\\"
    picklePrefix = "..\\indexes\\"
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
    if(finalRes):
        for top in sorted(finalRes, key=lambda x: finalRes[x]["score"], reverse=1)[:topK]:
            print(json.dumps({top:finalRes[top]}, indent=1))
    else:
        print({})
            
    print(f"operation took: {end - start}")


def simpleWildCardonOneFile(sampleInput):
    fileName = sampleInput["query"]["fileName"]
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    query = sampleInput["query"]["wildcard"]

    bigramIndex = openBigram(fileName)
    docInfo , invertedIndex = openOnePair(fileName)

    start = time.time()

    result = wildCardQuery(query, invertedIndex ,bigramIndex, topK)

    finalRes = {}
    
    end = time.time()

    if(result):
        for i in range(len(result)):
            finalRes[result[i][0]] = {"score":result[i][1],"document":docInfo[str(result[i][0])]}
    else:
        print("{}")
        
    print(json.dumps(finalRes,indent=1))
    print(f"operation took: {end - start}")

def simpleWildCardonAllFiles(sampleInput):
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    query = sampleInput["query"]["wildcard"]
    allIndexes = os.listdir("..\\indexes\\")
    allDocumentsInfo = os.listdir("..\\documentInfo\\")
    jsonPrefix = "..\\documentInfo\\"
    picklePrefix = "..\\indexes\\"
    allBigramIndexes = os.listdir("..\\bigramIndex\\")
    bigramPrefix =  "..\\bigramIndex\\"
    finalRes = {}

    start = time.time()
    
    for i in range(417):

        filePrefix = allDocumentsInfo[i][:-5]
        with open(jsonPrefix+filePrefix+".json", 'r') as f:
            docInfo = json.load(f)


        with open(picklePrefix+filePrefix+".pickle", 'rb') as file:
            invertedIndex = pickle.load(file)

        with open(bigramPrefix+filePrefix+".pickle", 'rb') as file:
            bigramIndex = pickle.load(file)


        result = wildCardQuery(query, invertedIndex ,bigramIndex, topK)

        for res in range(len(result)):
            finalRes[filePrefix + "_" +str(result[res][0])] = {"score":result[res][1],"document":docInfo[str(result[res][0])]}


    end = time.time()
    if(finalRes):
        for top in sorted(finalRes, key=lambda x: finalRes[x]["score"], reverse=1)[:topK]:
            print(json.dumps({top:finalRes[top]}, indent=1))
    else:
        print({})
    print(f"operation took: {end - start}")


if(sampleInput["query"]["mode"]):
    if("search" in sampleInput["query"]):
        AllfinalRes, timeTaken = simpleSearchOnAllFiles(sampleInput)
        # print(json.dumps(AllfinalRes,indent=1))
        print("\nTime taken by IR :", timeTaken)
    elif("must" in sampleInput["query"]):
        simplePhraseOnAllFiles(sampleInput)
    elif("wildcard" in sampleInput["query"]):
        simpleWildCardonAllFiles(sampleInput)
else:
    if("search" in sampleInput["query"]):
        OnefinalRes, timeTaken = simpleSearchOnOneFile(sampleInput)
        # print(json.dumps(OnefinalRes,indent=1))
        print("\nTime taken by IR :", timeTaken)
    elif("must" in sampleInput["query"]):
        simplePhraseOnOneFile(sampleInput)
    elif("wildcard" in sampleInput["query"]):
        simpleWildCardonOneFile(sampleInput)


AllDocInfo = os.listdir("..\\documentInfo\\")
if(COMPARE_MODE):
    if(sampleInput["query"]["mode"]==0):
        timing,esOutput = queryES(sampleInput)
        res = json.loads(esOutput)
        res = res["hits"]["hits"]
        id = []
        for i in range(len(res)):
            id.append(res[i]["_id"])
        print("Time taken By ES: "+str(timing))
        compareOutputs(OnefinalRes, id)
    else:
        times = []
        MaxScore = dict()
        final = dict()
        topK = sampleInput["query"]["top"]
        for i in range(417):
            filename = str(AllDocInfo[i][:-5])
            sampleInput["query"]["fileName"] = filename
            timing,result = queryES(sampleInput)
            res = json.loads(result)
            res = res["hits"]["hits"]
            for i in range(len(res)):
                score = res[i]["_score"]
                MaxScore[res[i]["_id"]] = {"score":score}
            times.append(timing)
        if(MaxScore):
            for top in sorted(MaxScore, key=lambda x: MaxScore[x]["score"], reverse=1)[:topK]:
                final[top] = MaxScore[top]
        id = final.keys()
        print("Time taken By ES: "+str(sum(times)))
        compareOutputs(AllfinalRes,id)

