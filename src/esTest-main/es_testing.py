import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd
from interface import Interface
from query_form import build_query
from spotify import Spotify

def execElasticSearch(inputs):
    es = Elasticsearch("http://localhost:9200")

    #print(es.info().body)
    print("-----------------------------------------------------------------------")
    print(inputs['answers'])
    print("-----------------------------------------------------------------------")
    songList =[]
    
    attributes = [0,0,0,0]
    for a in inputs['answers']:
        attributes.append(int(a))

    interface = Interface(attributes)
    finalAttributes = interface.prompt_user()

    
    
    q = build_query(finalAttributes)

    print("-----------------------------------------------------------------------")
    print(q)
    print("-----------------------------------------------------------------------")
    resp = es.search(index="songs", query=q)
    hits = (json.dumps(resp.body, indent=1))

    
    for x in range(len(resp.body["hits"]["hits"])):
       songList.append(resp.body["hits"]["hits"][x]["_source"]["track_id"])



    spotify = Spotify(songList)
    songs = spotify.search_ids()


    return (songs)
    
