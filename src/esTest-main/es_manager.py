from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd


class ESManager:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")
        # print(es.info().body)

    def create_index(self):
        """
        create_index creates the mappings for the index and the index "songs"
        :return: None
        """
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
        self.es.indices.create(index="songs", mappings=mappings)

    def populate_index(self):
        """
        populate_index loads the df and then uses bulk to populate the index "songs"
        :return: None
        """

        df = (
            pd.read_csv(".src/song_data_v4.csv")
            # drop missing values
            .dropna()
            .reset_index()
        )
        # push the data to the es index using bulk
        bulk_data = []
        for i, row in df.iterrows():
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
        bulk(self.es, bulk_data)
        # refresh the index
        self.es.indices.refresh(index="songs")
        # print the document count
        print(self.es.cat.count(index="songs", format="json"))

    def set_up_index(self):
        """
        set_up_index sets up the index for elastic search if the index does not already exist
        :return: None
        """
        if not self.es.indices.exists(index="songs"):
            self.create_index()
            self.populate_index()
