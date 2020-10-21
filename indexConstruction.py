from pandas import read_csv
from nltk.stem import WordNetLemmatizer 
from nltk import word_tokenize
from BTrees.OOBTree import OOBTree
from json import dump
import pickle
import sys

sys.setrecursionlimit(10000)


#Consts
csvFile = read_csv("combinedCSV.csv")
lemmatizer = WordNetLemmatizer()
invertedIndex = OOBTree()
docInfo = dict()
# TODO POS tagging and lemmatize based on pos

"""
lemmatizer = WordNetLemmatizer() 
  
print("rocks :", lemmatizer.lemmatize("rocks")) 
print("corpora :", lemmatizer.lemmatize("corpora")) 
  
# a denotes adjective in "pos" 
print("better :", lemmatizer.lemmatize("better", pos ="a"))
"""
# https://pythonhosted.org/BTrees/
# https://btrees.readthedocs.io/en/latest/api.html


def createDictionaryFromRow(row, headers):
    dictionary = { k:row[k] for k in headers }
    return dictionary


# iterate through all of the snippets in the dataset
for docId in range(len(csvFile)):
    #Json file for each doc { docID : { URL : "" , Snippet :""}}
    docInfo[docId] = createDictionaryFromRow(csvFile.iloc[docId], csvFile.columns)
    # tokenize the snippet to get all the words (using nltk word_tokenize function to do the same)
    #listOfWords = word_tokenize(csvFile['Snippet'][docId].lower())

    listOfWords = [x for x in word_tokenize(csvFile['Snippet'][docId].lower()) if x.isalnum()]
    for pos in range(len(listOfWords)):
        words = listOfWords[pos]
        lemWord = lemmatizer.lemmatize(words)
        #remove unwanted characters such -

        if(lemWord.isalnum()): 
            #if the word already exists in btree
            if(invertedIndex.has_key(lemWord)):
                #avoid repition of docIDs
                if(docId not in invertedIndex[lemWord][1]):
                    invertedIndex[lemWord][1][docId] = [1,[pos]]
                    invertedIndex[lemWord][0] += 1                    
                else:
                    invertedIndex[lemWord][1][docId][1].append(pos)
                    invertedIndex[lemWord][1][docId][0] += 1
            else:
                postingListElement = [1, {docId : [ 1, [pos]]}]
                invertedIndex.insert(lemWord, postingListElement)
    
# zero based postioning of words after removing non alpha numeric characters
# {
#   "the": 
#        [
#           123 #doc freq, 
    #       {
    #           1 #docID: [ 2 #term freq in doc, [12,112] #pos in doc], 2: [ 3 , [0, 12, 14]]
    #       }
#       ]
# }

"""
    {
        "the":
            123,
            object of linked list ------------> (1,4)->(2,4)
    }
"""
#print(invertedIndex["the"])
with open('csv1.pickle', 'wb') as handle:
   pickle.dump(invertedIndex, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('documentInfo.json', 'w') as f:
    dump(docInfo, f)
