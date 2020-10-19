from pandas import read_csv
from nltk.stem import WordNetLemmatizer 
from nltk import word_tokenize
from BTrees.OOBTree import OOBTree
import pickle

#Consts
csvFile = read_csv("/home/hp/Desktop/College/sem7/AIR/Project/TelevisionNews/BBCNEWS.201701.csv")
lemmatizer = WordNetLemmatizer()
invertedIndex = OOBTree()
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





for docId in range(len(csvFile['Snippet'])):
    for words in word_tokenize(csvFile['Snippet'][docId].lower()):
        lemWord = lemmatizer.lemmatize(words)
        if(lemWord.isalnum()):
            if(invertedIndex.has_key(lemWord)):
                if(docId not in invertedIndex[lemWord][1]):
                    invertedIndex[lemWord][1][docId] = 1
                    invertedIndex[lemWord][0] += 1
                else:
                    invertedIndex[lemWord][1][docId] += 1
            else:
                invertedIndex.insert(lemWord,[1, {docId:1}])

# {
#   "the": 
#        (
#           123, 
    #       {
    #           1: 4, 2: 4
    #       }
#       )
# }

"""
    {
        "the":
            123,
            object of linked list ------------> (1,4)->(2,4)
    }
"""
with open('csv1.pickle', 'wb') as handle:
    pickle.dump(invertedIndex, handle, protocol=pickle.HIGHEST_PROTOCOL)

