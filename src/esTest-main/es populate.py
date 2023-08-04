# es populate is the file to be run when a new session is started in docker
# go to command line and enter the following
# docker run --rm -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.7.0
# then run this file

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd
import os

# connect to the localhost
es = Elasticsearch("http://localhost:9200")
# prints out info about the connection
print(es.info().body)


# command to delete an index
# es.indices.delete(index='songs')
print(os.getcwd())
print("@@@@@@@@@@@@@@@@@@")
df = (
    pd.read_csv(".\src\esTest-main\song_data_v4.csv")
    # drop missing values
    .dropna()
    # only adding 5000 of the entries.
    #.sample(5000, random_state=42)
    .reset_index()
)

mappings = {
        "properties": {
            "track_id": {"type": "text", "analyzer": "english"},
            "artists": {"type": "text", "analyzer": "standard"},
            "album_name": {"type": "text", "analyzer": "standard"},
            "track_name": {"type": "text", "analyzer": "standard"},
            "popularity": {"type": "integer"},
            "explicit": {"type": "boolean"},
            "danceability": {"type": "float"},
            "energy": {"type": "float"}, 
            "loudness": {"type": "float"}, 
            "acousticness": {"type": "float"}, 
            "instrumentalness": {"type": "float"},
            "liveness": {"type": "float"},
            "valence": {"type": "float"}, 
            "tempo": {"type": "float"},
            "track_genre": {"type": "text", "analyzer": "english"}

    }
}
# create the index in elastic search
es.indices.create(index="songs", mappings=mappings)


# push the data to the es index using bulk
bulk_data = []
for i,row in df.iterrows():
    bulk_data.append(
        {
            "_index": "songs",
            "_id": i,
            "_source": {        
                "track_id": row["track_id"],
                "artists": row["artists"],
                "album_name": row["album_name"],
                "track_name": row["track_name"],
                "popularity": row["popularity"],
                "explicit": row["explicit"],
                "danceability": row["danceability"],
                "energy": row["energy"],
                "loudness": row["loudness"],
                "acousticness": row["acousticness"],
                "instrumentalness": row["instrumentalness"],
                "liveness": row["liveness"],
                "valence": row["valence"],
                "tempo": row["tempo"],
                "track_genre": row["track_genre"],
            }
        }
    )
bulk(es, bulk_data)

# refresh the index
es.indices.refresh(index="songs")

print("#####################################################################################")
# print the document count
print(es.cat.count(index="songs", format="json"))

print("#####################################################################################")
