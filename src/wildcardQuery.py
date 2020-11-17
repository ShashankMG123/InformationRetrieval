from utils import lemmatize_sentence,openOnePair

import json
import math
import pickle
from nltk.stem import WordNetLemmatizer 
from nltk import bigrams, pad_sequence
import time
from functools import reduce
import re

 # {
    #   "the": 
    #        [
    #           123 #doc freq, 
    #        {
    #            1:[2, [12, 112]], 2: [ 3 , [0, 12, 14]]
    #         }
    #       ]
# }

# *a --> a</s> 
# a* --> <s>a
# ab*cd -> intersection (ab, cd)
# *abv -> intersection ab bv v</s>
# *abc* -> intersection ab bc
# *a* -> <s>a a</s> 


def splitQuery(query):
    return(list(filter(lambda x: len(x) > 1, query.split("*"))))


def generateBiGramsForQuery(query):
    # Returns the bigrams from the query as a list.
    query = splitQuery("$"+query+"$") # *abc -> ab bc c$
    toReturn = []
    for i in range(len(query)):
        bigramKey = list(bigrams(list(pad_sequence(query[i],n=2))))               
        toReturn.extend(bigramKey)
    return toReturn

def getBiGrams(bigramIndex, listOfBigrams):
    toRet = []
    # given the bigram we retireve the posting list
    for bigram in listOfBigrams:
        toRet.append(bigramIndex.get(bigram))
    return toRet

def intersectionBiGrams(possibleWords):
    #  [['a'],['b'],['a']]
    # getting only the common matches 
    possibleWords = [x for x in possibleWords if x is not None]
    possibleWords = sorted(possibleWords, key= lambda x:len(x))
    return(list(reduce(lambda x,y: set(x) & set(y), possibleWords)))

def postFilter(regex, listOfCandi):
    # performing regex match
    regex = regex.replace("*", ".*")
    return list(filter(lambda x : re.search(regex, x), listOfCandi))

def wordRetrieval(query, bigramIndex):
    # generating bigrams for the query given as input
    biGramsForQuery = generateBiGramsForQuery(query) # $a ab intersection $ab  
    if(biGramsForQuery):
        # retrieving the posting list using the bigram index and the
        # bigrams generated for the query
        biGramLists = getBiGrams(bigramIndex,biGramsForQuery)
        # calling the intersection on the retrieved docs
        words = intersectionBiGrams(biGramLists)
        # peforming post filter on the retireved set
        filterWords = postFilter(query,words)
        return(filterWords)
    return([])
    
def documentRetrieval(invertedIndex, filterWords, topK):
    # our definition of top K is based on how many times it appears in
    # the resultant docs
    docDict = dict()
    for word in filterWords:
        for docs in invertedIndex.get(word)[1]:
            if docs in docDict:
                docDict[docs] += 1
            else:
                docDict[docs] = 1
    
    toReturn = []
    # returning the top K docs of all the matched results
    for i in sorted(docDict, key = docDict.get, reverse=True)[:topK]:
        toReturn.append((i,docDict[i]))
    return toReturn

        
def wildCardQuery(query, invertedIndex ,bigramIndex, topK):
   return(documentRetrieval(invertedIndex, wordRetrieval(query,bigramIndex), topK))
    
# *ab* -> '' 3.
#query = "*ec*" 
# *a*b*c*d*
# hi hi$ i$h $hi    xi --> xi$ i$x $xi          x*y -> y$x* > y$x > y$y  
# *ab*c* -----> $ab* intersection *c* ---> $c*
# $a ab c$ abc*-> $a ab bc 
# X*Y*Z -> Y$X* merge with Z$*
