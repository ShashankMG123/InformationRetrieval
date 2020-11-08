from utils import lemmatize_sentence

import json
import math
import pickle
from nltk.stem import WordNetLemmatizer 
from nltk import word_tokenize
import time

"""
sample input:
{
    query:
    {
        mode:0/1 0->look in file 1->look in all files
        fileName:"" -> filename without .csv
        search:"terms"
    }
}

{
    query:
    {
        must:"positional"
    }
}

{
    query:
    {
        wildcard:"abc*d"
    }
}
"""


# TF*IDF ranking


# {
#   "the": 
#        [
#           123 #doc freq (number of unique documents in which the term occurs), 
    #       {
    #           1 #docID: [ 2 #term freq in doc, [12,112] #pos in doc], 2: [ 3 , [0, 12, 14]]
    #       }
#       ]
# }


def getTokens(searchQuery):
    terms = lemmatize_sentence(searchQuery)
    return [term for term in terms if term.isalnum()]


def searchOnlyTerms(searchTerms, invertedIndex, topK, N):
    rankDict = {}
    searchTerms = getTokens(searchTerms)
    #N = max(invertedIndex,key=lambda x: int(x))
    #N = 279 #change based on len
    # iterating through all of the query terms
    for term in searchTerms:
        if(invertedIndex.has_key(term)):
            IDF = math.log(N/invertedIndex.get(term)[0] ,10)
            for docIDforTerm in invertedIndex[term][1]:
                if(docIDforTerm in rankDict):
                    rankDict[docIDforTerm] += invertedIndex.get(term)[1][docIDforTerm][0] * IDF
                else:
                    rankDict[docIDforTerm] = invertedIndex.get(term)[1][docIDforTerm][0] * IDF
        else:
            pass
    
    toReturn = []
    for i in sorted(rankDict, key =rankDict.get, reverse=True)[:topK]:
        toReturn.append((i,rankDict[i]))
    return toReturn

