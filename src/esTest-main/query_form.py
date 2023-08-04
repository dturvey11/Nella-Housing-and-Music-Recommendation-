# query_form provides the necessary functions for building a query from user's input
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd

es = Elasticsearch("http://localhost:9200")


def build_query(attribute_form):
    """
    build_query takes an attribute form and builds a query from atomic queries that has a must and should list
    :param attribute_form: a list of dictionaries that provide info on each attribute for the query
    :return: a query made up of atomic queries
    """
    must_list = []
    should_list = []

    # build individual queries to go in the big query
    for a in attribute_form:
        if a["attribute"] == "track_name" or a["attribute"] == "artists" or a["attribute"] == "album_name" or a["attribute"] == "track_genre" or a["attribute"] == "explicit":
            must_list.append(build_atomic_query(a['attribute'], a['match'], a['boolv'], a['phrase'], a['range'], a['val']))
        else:
            should_list.append(build_atomic_query(a['attribute'], a['match'], a['boolv'], a['phrase'], a['range'], a['val']))

    query = {"bool": {"must": must_list, "should": should_list}}
    # TODO: REMOVE THIS
    # print(query)
    return query


def build_atomic_query(attribute, match, boolv, phrase, rangev, val):
    """
    build_atomic_query takes info about an attribute and builds an atomic query
    :param attribute: the name of the attribute for the query
    :param match: a boolean value that determines if the query is a match query
    :param boolv: a boolean value that determines if the query is about a boolean attribute (the explicit attribute)
    :param phrase: when match is True, a string with the phrase to be matched, None when match is False
    :param rangev: a boolean value that determines if the query is a range query
    :param val: when rangev is True, an integer, None when rangev is False
    :return: an atomic query
    """
    atomic_query = None
    if match:
        atomic_query = {
            "match": {
                attribute: {
                    "query": phrase,
                    "fuzziness": 2,
                    "prefix_length": len(phrase)
                }
            }
        }
    elif boolv:
        atomic_query = {
            "match": {
                attribute: {
                    "query": phrase
                }
            }
        }
    elif rangev:
        atomic_query = {
            "range": {
                attribute: {
                    "gte": val - 0.2,
                    "lte": val + 0.2
                }
            }
        }

    return atomic_query


def build_song_att_form(song_dictionary, allow_explicit):
    """
    build_song_att_form takes information about a song in the form of a dictionary and whether explicit music is allowed
    to build an attribute form that is formatted so a query can be built from it
    :param song_dictionary: a dictionary of information on a song including danceability, energy, loudness, acousticness,
    instrumentallness, liveness, and tempo
    :param allow_explicit: is a boolean value that determines whether explicit music is allowed
    :return: an attribute form that is formatted as a dictionary with the proper keys
    """
    song_attr = []
    num_attributes = ["danceability", "energy", "loudness", "acousticness", "instrumentalness", "liveness", "valence",
                      "tempo"]
    if not allow_explicit:
        song_attr.append({"attribute": "explicit",
                                "match": False,
                                "boolv": True,
                                "phrase": "false",
                                "range": True,
                                "val": None
                                })
    for attr in num_attributes:
        song_attr.append({"attribute": attr,
                                "match": False,
                                "boolv": False,
                                "phrase": None,
                                "range": True,
                                "val": song_dictionary[attr]
                                })
    return song_attr


# ========EXAMPLES========

attributes1 = [
    {
        "attribute": "danceability",
        "match": False,
        "boolv": False,
        "phrase": None,
        "range": True,
        "val": 0.6
    },
    {
        "attribute": "energy",
        "match": False,
        "boolv": False,
        "phrase": None,
        "range": True,
        "val": 0.5
    },
    {
        "attribute": "explicit",
        "match": False,
        "boolv": True,
        "phrase": True,
        "range": False,
        "val": None
    }
]

attributes2 = [
    {
        "attribute": "artists",
        "match": True,
        "boolv": False,
        "phrase": "dua lipa",
        "range": False,
        "val": None
    }
]
