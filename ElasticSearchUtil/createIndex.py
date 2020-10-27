import requests
import json
import os
from pandas import read_csv


dataDir = "C:\\Users\\Shashank\\Desktop\\Project\\AIR\\TelevisionNews\\"
files = os.listdir(dataDir)

mappingJson = {
  "mappings": {
    "properties": {
      "URL": { "type": "text" },
      "MatchDateTime": { "type": "text" },
      "Station":{ "type": "text" },
      "Show":{ "type": "text" },
      "IAShowID": { "type": "text" },
      "IAPreviewThumb":{ "type": "text" },
      "Snippet":{ "type": "text" }
    }
  }
}

for i in files:

    csvFile = read_csv(dataDir+i)
    print(requests.delete("http://localhost:9200/"+i[:-4].lower()))
    print(requests.put("http://localhost:9200/"+i[:-4].lower(), json=mappingJson))
    contentJson = {}
    for doc in range(len(csvFile)):
        #{"index": {"_index": "teledataset", "_id": "0"}}
        indexJson = {"index":{"_index":i[:-4].lower(), "_id": str(doc) }}

        contentJson["URL"] = csvFile.iloc[doc]["URL"]
        contentJson["MatchDateTime"] = csvFile.iloc[doc]["MatchDateTime"]
        contentJson["Station"] = csvFile.iloc[doc]["Station"]
        contentJson["Show"] = csvFile.iloc[doc]["Show"]
        contentJson["IAShowID"] = csvFile.iloc[doc]["IAShowID"]
        contentJson["IAPreviewThumb"] = csvFile.iloc[doc]["IAPreviewThumb"]
        contentJson["Snippet"] = csvFile.iloc[doc]["Snippet"]

        with open('C:\\Users\\Shashank\\Desktop\\Project\\AIR\\InformationRetrieval\\ElasticSearchUtil\\jsonInputs\\'+i[:-4]+".json", 'a') as outfile:
            json.dump(indexJson,outfile)
            outfile.write("\n")
            json.dump(contentJson,outfile)
            outfile.write("\n")

    with open('C:\\Users\\Shashank\\Desktop\\Project\\AIR\\InformationRetrieval\\ElasticSearchUtil\\jsonInputs\\'+i[:-4]+".json", 'r') as outfile:
        headers = {'Content-Type': 'application/json'}
        postJson = outfile.read()
        print(requests.post("http://localhost:9200/_bulk",headers=headers, data=postJson))

    


