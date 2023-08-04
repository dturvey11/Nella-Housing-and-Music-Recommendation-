# es_execute is the file to run the entire Spotify Song Recommendation System
# first set up docker:
# go to command line and enter the following
# docker run --rm -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.7.0
# then run this file

import json
import jellyfish


from query_form import build_query, build_song_att_form
from es_manager import ESManager


def process_hits(r):
    """
    process_results takes results from an elastic search query and removes duplicate hits, returning a new dictionary
    :param r: the response from an elastic search query
    :return: a dictionary containing track id's and track names from the hits in the response
    """
    songs = []
    names = []
    for hit in r["hits"]["hits"]:
        add = True
        if names:
            for n in names:
                similarity = jellyfish.jaro_winkler_similarity(hit["_source"]["track_name"], n)
                if similarity >= 0.8:
                    add = False
        if add:
            names.append(hit["_source"]["track_name"])
            #songs.append({"track_id": hit["_source"]["track_id"], "track_name": hit["_source"]["track_name"]})
            songs.append(hit["_source"]["track_id"])
    return songs


def report_user_input(attributes):
    """
    report_user_input prints out the information collected from user utterances in a legible manner
    :param attributes: attributes built from user responses
    :return: none
    """
    for a in attributes:
        if a["match"] or a["boolv"]:
            print(a["attribute"], ": ", a["phrase"])
        elif a["range"]:
            print(a["attribute"], ": ", a["val"])


def set_up_elastic_search():
    es_man = ESManager()
    es_man.set_up_index()

    return es_man

def execute(prompt_man, es_man):

    q = build_query(prompt_man.attributes)
    if prompt_man.find_song:
        song = es_man.es.search(index="songs", query=q, sort="_score")
        if song["hits"]["total"]["value"] > 0:
            song_attributes = build_song_att_form(song["hits"]["hits"][0]["_source"], prompt_man.explicit)
            q = build_query(song_attributes)
        else:
            print("Sorry! We don't have that song.")

    # sort by popularity or by  highest score
    if prompt_man.popular_sort:
        resp = es_man.es.search(index="songs", query=q, sort="popularity:desc")
    else:
        resp = es_man.es.search(index="songs", query=q, sort="_score")

    if resp["hits"]["total"]["value"] > 0:
        processed_results = process_hits(resp)
        print(json.dumps(processed_results, indent=1))
        return processed_results
    else:
        print("Sorry! We didn't get any results from the following information: ")
        report_user_input(prompt_man.attributes)
        return report_user_input




