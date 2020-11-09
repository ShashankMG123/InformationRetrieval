from utils import lemmatize_sentence

import json
import math
import pickle
from nltk import word_tokenize
import time
from functools import reduce

  # {
    #   "the": 
    #        [
    #           123 #doc freq, 
        #       {
        #           1:[2, [12, 112]], 2: [ 3 , [0, 12, 14]]
        #       }
    #       ]
    # }


# [ {1:[1, [12]]} ,
#     {1:[2,[4, 24]] ,}
    
# ]
# docsToconsider = (1,)

def postFilter(docsToConsider, allDocList):
    docsToConsider = list(docsToConsider)
    
    positions = []
    """
    positions = []
    for ithWord in range(len(allDocList)):
        positions.append(dict())
        for doc in docsToConsider:
            positions[ithWord][doc]=allDocList[ithWord][1][doc][1]
    print(positions)
    """
    for doc in range(len(docsToConsider)):
        positions.append({})
        for ithWord in range(len(allDocList)):
            if(docsToConsider[doc] in positions[doc]):
                positions[doc][docsToConsider[doc]].append(allDocList[ithWord][1][docsToConsider[doc]][1])
            else:
                positions[doc][docsToConsider[doc]] = [allDocList[ithWord][1][docsToConsider[doc]][1]]
    
    #print(positions)
    
    docDict = {}

    for doc in positions:
        docID = list(doc.keys())[0]
        docCount = 0
        
        for i in doc[docID][0]:
            flag = 1
            for j in range(1,len(doc[docID])):
                if not(i+j in doc[docID][j]):
                    flag = 0
            if(flag):
                if(docID in docDict):
                    docDict[docID] += 1
                else:
                    docDict[docID] = 1
        
        
    return docDict
        # {40: [[54,78,97], [55]]}  
            
def intersection(listOfDictionaries):
    minDocDicts = sorted(listOfDictionaries, key=lambda i: i[0])
    # minDocDict = [{5:[1,13],6:[123]}] ---> (5,6)
    
    return(reduce(lambda a,b: set(a) & set(b), [minDocDict[1] for minDocDict in minDocDicts]))

    #return(reduce(lambda a,b: a & b, minDocDict))

def splitWords(sentence):
    words = [x for x in word_tokenize(sentence.lower())]
    lemWords = lemmatize_sentence(words)

    return lemWords
    
def fetchDocumentList(lemWords,invertedIndex):
    finalList = list()
    for word in lemWords:
        if(word in invertedIndex):
            finalList.append(invertedIndex[word])
        else:
            return [[0,{}]]
            
    return finalList
            

def searchPhrase(sentence, invertedIndex, topK):
    lemWords = splitWords(sentence)
    allDocList = fetchDocumentList(lemWords, invertedIndex)
    docsToConsider = intersection(allDocList)
    docDict = postFilter(docsToConsider,allDocList)
    toReturn = []
    for i in sorted(docDict, key = docDict.get, reverse=True)[:topK]:
        toReturn.append((i,docDict[i]))
    return toReturn
    

    
# fileName = "BBCNEWS.201701"
# with open(f"../indexes/{fileName}.pickle", 'rb') as file:
#         invertedIndex = pickle.load(file)

# with open(f'../documentInfo/{fileName}.json', 'r') as f:
#         docInfo = json.load(f)

# with open(f'../documentInfo/{fileName}.json', 'r') as f:
#         docInfo = json.load(f)
