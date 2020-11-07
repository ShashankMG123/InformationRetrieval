import requests


"""
http://localhost:9200/bbcnews.201701/_search?pretty=true&size=10
{
  "query": {
    "query_string": {
      "query": "teal",
      "default_field": "Snippet"
    }
  }
}
"""

def queryES(sampleInput):
    payload = {
                "query": {
                    "query_string": {
                        "query": " ".join(sampleInput["query"]["search"]),
                       "default_field": "Snippet"
                    }
                }
                }
    response = requests.get(f'http://localhost:9200/{sampleInput["query"]["fileName"].lower()}/_search?pretty=true&size={ sampleInput["query"]["top"]}',json = payload)
    timing = response.elapsed.total_seconds()

    return(timing,response.text)

# sampleInput = {
#                     "query":
#                     {
#                         "mode":0,
#                         "fileName" : "FOXNEWS.201001",
#                         "search" : ["hi"],
#                         "top":3
#                     }
#                 }

# queryES(sampleInput)