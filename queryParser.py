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
    lemmatizer = WordNetLemmatizer()
    terms = [lemmatizer.lemmatize(word) for word in word_tokenize(searchQuery)] 
    return [term for term in terms if term.isalnum()]


def searchOnlyTerms(jsonInput, invertedIndex, topK):
    rankDict = {}
    searchTerms = getTokens(jsonInput["query"]["search"].lower())
    N = 94858
    #N = 279 #change based on len
    # iterating through all of the query terms
    for term in searchTerms:
        IDF = math.log(N/invertedIndex[term][0] ,10)
        for docIDforTerm in invertedIndex[term][1]:
            if(docIDforTerm in rankDict):
                rankDict[docIDforTerm] += invertedIndex[term][1][docIDforTerm][0] * IDF
            else:
                rankDict[docIDforTerm] = invertedIndex[term][1][docIDforTerm][0] * IDF
                
    return sorted(rankDict, key =rankDict.get, reverse=True)[:topK]

    

with open("csv2.pickle", 'rb') as file:
    invertedIndex = pickle.load(file)


sampleInput = {
                    "query":
                    {
                        "search":"pollution"
                    }
                }


with open('documentInfo.json', 'r') as f:
    docInfo = json.load(f)

# print(max(invertedIndex["the"][1],key = lambda x: invertedIndex["the"][1][x][0]))

start = time.time()

result = searchOnlyTerms(sampleInput, invertedIndex, 2)

end = time.time()

for docId in result:
    print(docInfo[str(docId)])


print(f"operation took: {end - start}")
