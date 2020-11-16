from utils import openOnePair, openBigram, compareOutputs
from simpleSearch import searchOnlyTerms
from phraseQuery import searchPhrase
from wildcardQuery import wildCardQuery
from compareES import queryES
import json
import pickle
import time
import os
import sys


COMPARE_MODE = int(sys.argv[2])
  
InputFileName = sys.argv[1]


with open(f'input\\{InputFileName}.json', 'r') as handle:
    sampleInput = json.load(handle)

"""
This function is for performing simple word based search
we are not testing the positional information
checking if the list of words passed as input present in the 
filename given as input
"""
def simpleSearchOnOneFile(sampleInput):

    fileName = sampleInput["query"]["fileName"]
    docInfo , invertedIndex = openOnePair(fileName)
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = [searchTerm.lower() for searchTerm in sampleInput["query"]["search"]]

    start = time.time()
    # calling the searching function
    # takes input as query terms , inverted index , K results needed
    result = searchOnlyTerms(searchTerms, invertedIndex, topK, max([int(x) for x in docInfo]))

    end = time.time()

    finalRes = {}
    for i in range(len(result)):
        finalRes[result[i][0]] = {"score":result[i][1],"document":docInfo[str(result[i][0])]}
                        
    return(finalRes, (end - start))
    


"""
This function is for performing simple word based search
we are not testing the positional information
checking if the list of words passed as input present in all
the files
"""
def simpleSearchOnAllFiles(sampleInput):

    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = [searchTerm.lower() for searchTerm in sampleInput["query"]["search"]]
    allDocumentsInfo = os.listdir("..\\documentInfo\\")
    jsonPrefix = "..\\documentInfo\\"
    picklePrefix = "..\\indexes\\"
    finalRes = {}

    start = time.time()
    # reading each file one by one
    for i in range(417):

        filePrefix = allDocumentsInfo[i][:-5]
        
        with open(jsonPrefix+filePrefix+".json", 'r') as f:
            docInfo = json.load(f)


        with open(picklePrefix+filePrefix+".pickle", 'rb') as file:
            invertedIndex = pickle.load(file)

        # calling the search function
        # takes query terms, inverted index, K value as input
        result = searchOnlyTerms(searchTerms, invertedIndex, topK , max([int(x) for x in docInfo]))

        # returns top K docs from each file
        for res in range(len(result)):
            finalRes[result[res][0]] = {"docName":filePrefix + "_" +str(result[res][0]) ,"score":result[res][1],"document":docInfo[str(result[res][0])]}

    end = time.time()

    FinalRes = dict()
    # we need overall top K docs
    # so we pick up the top K from the sorted collection 
    # of all docs retrieved from each file
    if(finalRes):
        for top in sorted(finalRes, key=lambda x: finalRes[x]["score"], reverse=1)[:topK]:
            FinalRes[top] = finalRes[top]

    return (FinalRes,(end - start))

"""
This function is for performing phrase search on one file
we are considering the positional information as well
takes a phrase(set of words) as input and searches it in
a particular file given as input
"""
def simplePhraseOnOneFile(sampleInput):
    fileName = sampleInput["query"]["fileName"]
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = sampleInput["query"]["must"]

    docInfo , invertedIndex = openOnePair(fileName)
    start = time.time()

    # calling the search function
    # takes input as the phrase (set of words), inverted index , K value
    result = searchPhrase(searchTerms, invertedIndex, topK)

    finalRes = {}
    end = time.time()
    
    for i in range(len(result)):
        finalRes[result[i][0]] = {"score":result[i][1],"document":docInfo[str(result[i][0])]}
                        
    print(json.dumps(finalRes,indent=1))
    print(f"operation took: {end - start}")

"""
This function is for performing phrase search on all the
files. Takes in a phrase(set of words) as input and searches 
it in all files
"""
def simplePhraseOnAllFiles(sampleInput):
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    searchTerms = sampleInput["query"]["must"]
    allDocumentsInfo = os.listdir("..\\documentInfo\\")
    jsonPrefix = "..\\documentInfo\\"
    picklePrefix = "..\\indexes\\"
    finalRes = {}

    start = time.time()
    # reading each file one by one
    for i in range(417):

        filePrefix = allDocumentsInfo[i][:-5]
        with open(jsonPrefix+filePrefix+".json", 'r') as f:
            docInfo = json.load(f)


        with open(picklePrefix+filePrefix+".pickle", 'rb') as file:
            invertedIndex = pickle.load(file)

        # calling the search function
        # input parameters are the phrase, inverted index, K value
        result = searchPhrase(searchTerms, invertedIndex, topK)

        # retrieves top K from each file
        for res in range(len(result)):
            finalRes[result[res][0]] = {"docName":filePrefix + "_" +str(result[res][0]),"score":result[res][1],"document":docInfo[str(result[res][0])]}

    end = time.time()
    print(f"operation took: {end - start}")
    # selecting the overall top K docs 
    if(finalRes):
        for top in sorted(finalRes, key=lambda x: finalRes[x]["score"], reverse=1)[:topK]:
            print(json.dumps({top:finalRes[top]}, indent=1))
    else:
        print({})
            

"""
This function is for performing wildcard query search
it takes input as the wildcard and a particular filename 
to search in
"""
def simpleWildCardonOneFile(sampleInput):
    fileName = sampleInput["query"]["fileName"]
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    query = sampleInput["query"]["wildcard"]
    bigramIndex = openBigram(fileName)
    docInfo , invertedIndex = openOnePair(fileName)

    start = time.time()

    # calling the search function
    # input is the wildcard query , inverted index, bigram index, K value
    result = wildCardQuery(query, invertedIndex ,bigramIndex, topK)
    
    end = time.time()
    print(f"operation took: {end - start}")
    finalRes = {}
    if(result):
        for i in range(len(result)):
            finalRes[result[i][0]] = {"score":result[i][1],"document":docInfo[str(result[i][0])]}
    else:
        print("{}")
        
    print(json.dumps(finalRes,indent=1))

"""
This function is for performing wildcard query
on all the files present.
input is the wildcard query
"""
def simpleWildCardonAllFiles(sampleInput):
    topK = sampleInput["query"]["top"] if "top" in sampleInput["query"] else 5
    query = sampleInput["query"]["wildcard"]
    allDocumentsInfo = os.listdir("..\\documentInfo\\")
    jsonPrefix = "..\\documentInfo\\"
    picklePrefix = "..\\indexes\\"
    bigramPrefix =  "..\\bigramIndex\\"
    finalRes = {}

    start = time.time()
    # reading each file one by one
    for i in range(417):

        filePrefix = allDocumentsInfo[i][:-5]
        with open(jsonPrefix+filePrefix+".json", 'r') as f:
            docInfo = json.load(f)


        with open(picklePrefix+filePrefix+".pickle", 'rb') as file:
            invertedIndex = pickle.load(file)

        with open(bigramPrefix+filePrefix+".pickle", 'rb') as file:
            bigramIndex = pickle.load(file)

        # calling the search function
        # inputs are query, inverted index, bigram index, K value
        result = wildCardQuery(query, invertedIndex ,bigramIndex, topK)
        # it retrieves top K from each file
        for res in range(len(result)):
            finalRes[result[res][0]] = {"docName":filePrefix + "_" +str(result[res][0]),"score":result[res][1],"document":docInfo[str(result[res][0])]}

    end = time.time()
    print(f"operation took: {end - start}")
    # selecting the overall top K from all the files considered
    if(finalRes):
        for top in sorted(finalRes, key=lambda x: finalRes[x]["score"], reverse=1)[:topK]:
            print(json.dumps({top:finalRes[top]}, indent=1))
    else:
        print({})

# calling respective search functions 
# based on the input json fields
if(sampleInput["query"]["mode"]):
    if("search" in sampleInput["query"]):
        AllfinalRes, timeTaken = simpleSearchOnAllFiles(sampleInput)
        print("\nTime taken by IR :", timeTaken)
        print(json.dumps(AllfinalRes,indent=1))
    elif("must" in sampleInput["query"]):
        simplePhraseOnAllFiles(sampleInput)
    elif("wildcard" in sampleInput["query"]):
        simpleWildCardonAllFiles(sampleInput)
else:
    if("search" in sampleInput["query"]):
        OnefinalRes, timeTaken = simpleSearchOnOneFile(sampleInput)
        print("\nTime taken by IR :", timeTaken)
        # print(json.dumps(OnefinalRes,indent=1))
    elif("must" in sampleInput["query"]):
        simplePhraseOnOneFile(sampleInput)
    elif("wildcard" in sampleInput["query"]):
        simpleWildCardonOneFile(sampleInput)

# this portion is basically for comparing
# Elastic Search with out Information Retrieval engine
AllDocInfo = os.listdir("..\\documentInfo\\")
if(COMPARE_MODE):
    if(sampleInput["query"]["mode"]==0):
        # querying the Elastic Search
        timing,esOutput = queryES(sampleInput)
        res = json.loads(esOutput)
        res = res["hits"]["hits"]
        id = []
        for i in range(len(res)):
            id.append(res[i]["_id"])
        print("Time taken By ES: "+str(timing))
        # comparing the 2 results and printing the confusion matrix
        # other metrics
        compareOutputs(OnefinalRes, id)
    else:
        times = []
        MaxScoreOverall = dict()
        final = dict()

        topK = sampleInput["query"]["top"]
        for i in range(417):
            filename = str(AllDocInfo[i][:-5])
            sampleInput["query"]["fileName"] = filename
            # querying the Elastic Search
            timing,result = queryES(sampleInput)
            res = json.loads(result)
            res = res["hits"]["hits"]
            MaxScorePerFile = dict()
            for i in range(len(res)):
                score = res[i]["_score"]
                MaxScorePerFile[res[i]["_id"]] = {"score":score}
            if(MaxScorePerFile):
                for top in sorted(MaxScorePerFile, key=lambda x: MaxScorePerFile[x]["score"], reverse=1)[:topK]:
                    MaxScoreOverall[top] = MaxScorePerFile[top]
            times.append(timing)
        if(MaxScoreOverall):
            for top in sorted(MaxScoreOverall, key=lambda x: MaxScoreOverall[x]["score"], reverse=1)[:topK]:
                final[top] = MaxScoreOverall[top]
        id = final.keys()

        print("Time taken By ES: "+str(sum(times)))
        # comparing the 2 results and printing the confusion matrix
        # other metrics
        compareOutputs(AllfinalRes,id)

