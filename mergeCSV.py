import os
import glob
import pandas as pd

all_filenames = os.listdir("TelevisionNews")
#print(all_filenames)

#combine all files in the list
combined_csv = pd.concat([pd.read_csv("TelevisionNews\\" + f ) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combinedCSV.csv", index=False, encoding='utf-8')
