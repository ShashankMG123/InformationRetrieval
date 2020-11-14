from utils import lemmatize_sentence

from pandas import read_csv
from nltk.stem import WordNetLemmatizer 
from nltk import word_tokenize
from BTrees.OOBTree import OOBTree
from json import dump
import pickle
import sys
import os


#Consts
#csvFile = read_csv("combinedCSV.csv")

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

def createIndex(csvFileName):
# iterate through all of the snippets in the dataset
    # Creating a BTree structure to hold the inverted index
    invertedIndex = OOBTree()
    # a dictionary to hold the document information
    docInfo = dict()
    csvFile = read_csv(f"..\..\TelevisionNews\{csvFileName}")
    for docId in range(len(csvFile)):
        # Json file for each doc { docID : { URL : " " , Snippet :"",....}}
        docInfo[docId] = createDictionaryFromRow(csvFile.iloc[docId], csvFile.columns)
       
        # tokenize the snippet to get all the words (using nltk word_tokenize function to do the same)
        # listOfWords = word_tokenize(csvFile['Snippet'][docId].lower())
        listOfWords = [x for x in word_tokenize(csvFile['Snippet'][docId].lower()) if x.isalnum()]
        listOfWords = lemmatize_sentence(listOfWords)

        for pos in range(len(listOfWords)):
            lemWord = listOfWords[pos]
            # lemWord = lemmatizer.lemmatize(words)
            # remove unwanted characters such -

            if(lemWord.isalnum()): 
                # if the word already exists in BTree
                if(invertedIndex.has_key(lemWord)):
                    # avoid repeatition of docIDs
                    if(docId not in invertedIndex[lemWord][1]):
                        invertedIndex[lemWord][1][docId] = [1,[pos]]
                        invertedIndex[lemWord][0] += 1                    
                    else:
                        invertedIndex[lemWord][1][docId][1].append(pos)
                        invertedIndex[lemWord][1][docId][0] += 1
                else:
                    postingListElement = [1, {docId : [ 1, [pos]]}]
                    invertedIndex.insert(lemWord, postingListElement)

    # writing the inverted index into pickele file
    # one pickle file for each csv
    with open(f'..\indexes\{csvFileName[:-4]}.pickle', 'wb') as handle:
        pickle.dump(invertedIndex, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # dumping the docInfo of each csv file into a json file
    with open(f'..\documentInfo\{csvFileName[:-4]}.json', 'w') as f:
        dump(docInfo, f)

# reading all the csv files one by one 
# and calling the create index function
all_filenames = os.listdir("..\..\TelevisionNews\\")
for i in range(len(all_filenames)):
    createIndex(all_filenames[i])


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

    #     {
    #         "the":
    #             123,
    #             object of linked list ------------> (1,4)->(2,4)
    #     }