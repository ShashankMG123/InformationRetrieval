from os import system as sys
from os import chdir

sys("mkdir bigramIndex documentInfo indexes ElasticSearchUtil/jsonInputs")
chdir("src")
sys("python3 indexConstruction.py")
sys("python3 generateBigramIndex.py")
chdir("../ElasticSearchUtil")
sys("python3 createIndex.py")