# command line interface for the updated dialogue flow
import json
import openai
import random
from prompts import prompts
from entailment import get_attribute_numbers

openai.api_key = "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"


def get_llm_response(llm_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model="gpt-4",
            messages=[{"role": "user", "content": llm_prompt}],
            temperature=0.2,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2,
            timeout=5
            # stop="stop"
        )
    except Exception as e:
        print("Exception {}".format(e))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model="gpt-4",
            messages=[{"role": "user", "content": llm_prompt}],
            temperature=0.2,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2,
            timeout=5
            # stop="stop"
        )
    return response["choices"][0]["message"]["content"]

def build_song_dict(songs):
    """
    build_song_dict takes a list of songs and makes a dictionary with the appropriate info
    :param songs: a list of songs
    :return: a dictionary for the songs
    """
    s_list = ""
    for s in songs:
        s_list = s_list + " " + s
    return {
        "attribute": "track_name",
        "match": True,
        "boolv": False,
        "phrase": s_list,
        "range": False,
        "val": None
    }


def build_artist_dict(artists):
    """
    build_artist_dict takes a list of artists and makes a dictionary with the appropriate info
    :param artists: a list of artists
    :return: a dictionary for the artists
    """
    a_list = ""
    for a in artists:
        a_list = a_list + " " + a
    return {
        "attribute": "artists",
        "match": True,
        "boolv": False,
        "phrase": a_list,
        "range": False,
        "val": None
    }


def build_album_dict(albums):
    """
    build_album_dict takes a list of albums and makes a dictionary with the appropriate info
    :param albums: a list of albums
    :return: a dictionary for the albums
    """
    a_list = ""
    for a in albums:
        a_list = a_list + " " + a
    return {
        "attribute": "album_name",
        "match": True,
        "boolv": False,
        "phrase": a_list,
        "range": False,
        "val": None
    }


def build_genre_dict(genres):
    """
    build_genre_dict takes a list of genres and makes a dictionary with the appropriate info
    :param genres: a list of genres
    :return: a dictionary for the genres
    """
    g_list = ""
    for g in genres:
        g_list = g_list + " " + g
    return {
        "attribute": "track_genre",
        "match": True,
        "boolv": False,
        "phrase": g_list,
        "range": False,
        "val": None
    }



class PromptManager:
    def __init__(self):
        self.attributes = []
        self.explicit = True
        self.popular_sort = False
        self.find_song = False
        self.prompt_number = 0
        self.continue_flag  = True
        self.response = ""

    def build_new(self):
        self.__init__()


    def get_current_prompt(self):

        prompt = "Please see recommendations on the left"
        if self.prompt_number < 7:
            match self.prompt_number:
                case 0:
                    prompt = random.sample(prompts["intro"], 1)[0]
                case 1:
                    prompt = random.sample(prompts["explicit"], 1)[0]
                case 2:
                    prompt = random.sample(prompts["popularity"], 1)[0]
                case 3:
                    prompt = random.sample(prompts["specifics"], 1)[0]
                case 4:
                    prompt = "Would you like to continue narrowing your search or search with just the current parameters you have given?"
                case 5:
                    if self.continue_flag:
                        prompt = "What do you want from this song?"
                    else:
                        prompt = "Please see recommendations on the left"

        self.prompt_number = self.prompt_number + 1

        
        return prompt

    def prompt_user(self):
        
        """
        prompt_user calls each function that prompts user for specific information and compiles a list of dictionaries
        to be used for query
        :return: None
        """
        # TODO: FRONT END HANDLES INTRO PROMPT
        
        if self.prompt_number < 7: 
            print(str(self.prompt_number) + '@@@@@@@@@@@@@')
            match self.prompt_number:
                case 0:
                    print("one")
                case 1:
                    print("two")
                case 2:
                    print(self.attributes)
                    explicit_att = self.explicit_prompt()
                    print("###############")
                    print(explicit_att)
                    if explicit_att:
                        self.explicit = False
                        self.attributes.append(explicit_att)
                        print(self.attributes)
                case 3:
                    self.popular_sort = self.popularity_prompt()
                case 4:
                    s_list = self.specifics_prompt()
                    if s_list:
                        
                        for attribute in s_list:
                            if attribute["attribute"] == "track_name":
                                self.find_song = True
                            self.attributes.append(attribute)
                case 5:
                    self.continue_flag = self.continue_prompt()
                case 6:
                    if(self.continue_flag):
                        #feels prompt             
                        att_list = self.feels_prompt()
                        if(att_list):
                            for attribute in att_list: 
                                self.attributes.append(attribute)

        return self.get_current_prompt()
        

       
        
        
  
        



    def intro_prompt(self):
        """
        intro_prompt prints a random intro to the user
        :return None
        """
        print(random.sample(prompts["intro"], 1)[0])


    def explicit_prompt(self):
        """
        explicit_prompt asks a user if they are okay with explicit music results
        only adds an attribute to the list if they are not
        :return: a dictionary saying the explicit attribute is false when users enter no, and None when yes is entered
        """
        print(random.sample(prompts["explicit"], 1)[0])

        print(self.response['message'])
        explicit = self.response['message']
        llm_prompt = "Identify whether the response that is delimited by the triple backticks indicates that explicit music is allowed or not allowed based on whether the response is positive or negative. " \
                    "A positive response indicates explicit music is allowed, a negative response means explicit music is not allowed. " \
                    "Format the response as a json string in the following format: {\"explicit\": EXPLICIT} where EXPLICIT is either true or false. " \
                    "If the response is irrelevant empty or invalid return a json string in the following format: {\"response\":  -1}. " \
                    "Do not provide anything other than the json.\n'''" + explicit + "'''"

        resp_json = get_llm_response(llm_prompt)
        resp_dict = json.loads(resp_json)

        if "response" not in resp_dict:
            if not resp_dict["explicit"]:
                return {
                    "attribute": "explicit",
                    "match": False,
                    "boolv": True,
                    "phrase": "false",
                    "range": False,
                    "val": None
                }
            else:
                return None

        else:
            print(
                "Invalid response: no specification of explicitness has been requested. "
                "Explicit music will be allowed as a default.")



    def popularity_prompt(self):
        """
        popularity_prompt asks the user if they would prefer to have their results sorted by popularity
        :return: a boolean value of true if user responds yes and a value of false if 'no' is entered
        """
        print()
        popularity = self.response['message']
        llm_prompt = "Identify whether the response that is delimited by the triple backticks indicates that popular music would be preferred or not based on whether the response is positive or negative. " \
                    "A neutral or positive response indicates popular music is preferred, a negative response means popular music is not preferred. " \
                    "Format the response as a json string in the following format: {\"popularity\": POPULARITY} where POPULARITY is either true or false. " \
                    "If the response is irrelevant empty or invalid return a json string in the following format: {\"response\":  -1}. " \
                    "Do not provide anything other than the json.\n'''" + popularity + "'''"

        resp_json = get_llm_response(llm_prompt)
        resp_dict = json.loads(resp_json)

        if "response" not in resp_dict:
            if not resp_dict["popularity"]:
                return False
            else:
                return True

        else:
            print(
                "Invalid response: no specification of popularity has been requested. "
                "Music will be sorted by popularity as a default.")
            return True




    def continue_prompt(self):
        """
        continue_prompt asks the user if they want to continue refining their search or not
        :return: a boolean value that is True if the user wants to continue, and False if not
        """
        print()
        cont = self.response['message']
        llm_prompt = "Identify whether the response that is delimited by the triple backticks indicates that the search should continue or not based on whether the response is positive or negative. " \
                    "A neutral or positive response indicates the search should continue, a negative response means the search should not continue. " \
                    "Format the response as a json string in the following format: {\"cont\": CONT} where CONT is either true or false. " \
                    "If the response is irrelevant empty or invalid return a json string in the following format: {\"response\":  -1}. " \
                    "Do not provide anything other than the json.\n'''" + cont + "'''"

        resp_json = get_llm_response(llm_prompt)
        resp_dict = json.loads(resp_json)

        if "response" not in resp_dict:
            if resp_dict["cont"]:
                self.continue_flag = True
                return True
            else:
                self.continue_flag = False
                return False
        else:
            print("Invalid response: Search will continue as a default.")
            self.continue_flag = True
            return True




    def feels_prompt(self):
        print("")
        uttr = self.response['message']

        attr_list = get_attribute_numbers(uttr)

        return attr_list
    
    def specifics_prompt(self):
        """
        specifics_prompt asks the user whether there are any specific artists, albums, songs, or genres
        that they want to listen to
        :return: list of dictionaries of any attributes specified
        """
        specifics = []

        print()
        user_in = self.response['message']
        llm_prompt = "Identify any specific song titles, artists, albums, and genres from the given response that is delimited by the triple backticks. " \
                    "Format the response as a json string in the following format: {\"songs\": SONGS, \"artists\": ARTISTS, \"albums\": ALBUMS, \"genres\": GENRES}. " \
                    "If there are no songs, artists, albums, or genres identified in the response or the response is irrelevant, empty or invalid return a json string in the following format: {\"response\":  -1}. " \
                    "The fields should be lists of the identified songs, artists, albums, and genres as strings. " \
                    "If any of the fields are empty make their value just -1. " \
                    "For example, if there were no songs mentioned the songs field would be: \"songs\": -1.. " \
                    "Do not provide anything other than the json.\n'''" + user_in + "'''"

        resp_json = get_llm_response(llm_prompt)
        resp_dict = json.loads(resp_json)

        if "response" not in resp_dict:
            if resp_dict["artists"] != -1:
                specifics.append(build_artist_dict(resp_dict["artists"]))
            if resp_dict["songs"] != -1:
                specifics.append(build_song_dict(resp_dict["songs"]))
            if resp_dict["albums"] != -1:
                specifics.append(build_album_dict(resp_dict["albums"]))
            if resp_dict["genres"] != -1:
                specifics.append(build_genre_dict(resp_dict["genres"]))
        else:
            print("No specific songs, artists, albums, or genres have been requested.")
            specifics = None

        return specifics




        
        
