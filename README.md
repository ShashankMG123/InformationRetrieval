# InformationRetrieval

## Problem

* Build a search engine for Environmental News NLP archieve.

* Built a corpus for archieve with atleast 418 documents.

----

## Dataset

* <https://www.kaggle.com/amritvirsinghx/environmental-news-nlp-dataset>

----

## Setup instructions

* clone the git repo <https://github.com/ShashankMG123/InformationRetrieval.git>
* ``` cd InformationRetrieval ```
* ``` python3 setup.py ```

## Libraries used

* nltk
* BTrees

Set up these Libraries for your system.

## File structure

<pre>

├── 0226_0286_0298_1557_AIR_Report.pdf
├── bigramIndex
├── documentInfo
├── ElasticSearchUtil
│   ├── createIndex.py
│   └── jsonInputs
├── indexes
├── README.md
├── setup.py
└── src
    ├── input
        ├── SimpleSearch.json
        ├── PhraseSearch.json
        └── WildCard.json
    ├── compareES.py
    ├── genetateBigramIndex.py
    ├── indexConstruction.py
    ├── phraseQuery.py
    ├── queryDriver.py
    ├── simpleSearch.py
    ├── utils.py
    └── wildcardQuery.py
</pre>

## Input variations

mode :

* 0 (Single File search)
* 1 (All File search)

fileName : Name of file if mode 0
search : list of terms for simple search
must : phrase for positional search
wildcard : for wildcard query
top : number of docs required

## Running the IR system

* Change the json file in the input directory
* ``` python3 queryDriver.py <type of query> <compare with ES flag> ```
 If compare flag is on make sure ES has started with all indexes running on port 9200.
 sample command ```python3 queryDriver.py SimpleSearch 0```
