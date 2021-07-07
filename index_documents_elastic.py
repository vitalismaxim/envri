from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from glob import glob
import json

es = Elasticsearch("http://localhost:9200")

# path is correct IF this file is in the same folder as 'envri_json' 
folders = glob("envri_json/*")

#print(folders)
#print(len(folders))

filelist = []
for i in range(len(folders)):
    folder = folders[i] + "/*"
    filelist.append(glob(folder))

filelist = [file for folder in filelist for file in folder]
#print(filelist)

sample = filelist
completed = len(sample) # counter

#----------------------------------------------------------------

def open_file(file):
    read_path = file
    with open(read_path, "r", errors='ignore') as read_file:
        data = json.load(read_file)
    return data


def index_elastic():
    indexed = 0
    for i in range(len(sample)):
        doc = open_file(sample[i])
        id = doc["identifier"]
        print(round(((i + 1) / completed * 100), 2), "%", sample[i]) # keep track of progress / counter
        indexed += 1
        res = es.index(index = "envri", id = doc["identifier"], body=doc)
        es.indices.refresh(index = "envri")

index_elastic()

#----------------------------------------------------------------------
