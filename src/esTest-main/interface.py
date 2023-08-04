
class Interface():
    # command line interface for nella song side of things 

    def __init__(self, inputs):
        self.inputs = inputs

        self.attributes = inputs 
        print("construcor")
        print(self.attributes)
    #attributes is the list of attributes in the format to be searched in elasticsearch. 
    

    # explicit #####
    def explicit_input(self): 
        print("Do you want to include explicit results in this search?")
        print("0 for no, 1 for yes")

        explicit = self.inputs[0]

        if(explicit):

            return {
                    "attribute": "explicit",
                    "match": False,
                    "boolv": True,
                    "phrase": "true",
                    "range": False,
                    "val": None
                }
            
        else:
            return {
                    "attribute": "explicit",
                    "match": False,
                    "boolv": True,
                    "phrase": "false",
                    "range": False,
                    "val": None
                }



    # artist #####
    def artist_input(self): 
        print("Enter the name of the artist")
        print("(if there are multiple names, separate them with a comma)")
        artist_name = input()

        return {
                "attribute": "artist", 
                "match": True,
                "boolv": False,
                "phrase": artist_name, 
                "range": False,
                "val": None
            }




    # album #####
    def album_input(): 

        print("Enter the name of the album")
        album_name = input()

        return {"attribute": "album_name", 
                "match": True,
                "boolv": False,
                "phrase": album_name, 
                "range": False,
                "val": None
            }



    # genre #####
    # has a loop to take in genres, stores them in an array. 
    def genre_input(self):

        print("Choose a genre of music, you can enter multiple")
        print("if done, hit enter")

        genre_choice = input()
        genres = []

        while(genre_choice != ""):
            genres.append(genre_choice)
            print("Add another genre?")
            genre_choice = input()

        if genres != []:

            genre_string = genres.pop(0)

            for x in genres:
                genre_string += " OR " + x 

            return {
                    "attribute": "genre", 
                    "match": True,
                    "boolv": False,
                    "phrase": genre_string, 
                    "range": False,
                    "val": None
                }
        else: 
            return 0 
            


    ######### NUMBERS #####

    # valence #####

    def valence_input(self): 
        print("On a scale of 0 to 10, how do you want to feel after hearing this song?")
        print("(0 being sad/bad and 10 being happy/good)")

        valence = self.attributes[4]

        valence *= 0.1 

        return {
                "attribute": "valence", 
                "match": False,
                "boolv": False,
                "phrase": None, 
                "range": True, 
                "val": valence 
            }



    # dancibility #####

    def danceability_input(self):
        print("On a scale of 0 to 10, how much do you feel like dancing?")
        print("( 0 being not at all and 10 being I WANNA DANCE)")

        danceability = self.attributes[5]

        danceability *= 0.1 

        return {
                "attribute": "danceability", 
                "match": False,
                "boolv": False,
                "phrase": None, 
                "range": True, 
                "val": danceability
            }

    # energy #####

    def energy_input(self): 
        print("On a scale of 0 to 10, how much energy do you want from a song rn?")
        print("( 0 being not nuch energy and 10 being all the enegry there is)")

        energy = self.attributes[6]

        energy *= 0.1 

        return {
                "attribute": "energy", 
                "match": False,
                "boolv": False,
                "phrase": None, 
                "range": True, 
                "val": energy
            }

    # loudness ##### 

    def loudness_input(self): 
        print("How loud do you want the song to be?")
        print("( 0 being quiet and 10 being loud)")

        loudness = self.attributes[7]

        loudness *= 0.1 

        return {
                "attribute": "loudness", 
                "match": False,
                "boolv": False,
                "phrase": None, 
                "range": True, 
                "val": loudness
            }

    # acousticness ###### 

    def acousticness_input(self): 
        print("On a scale of 0 to 10, how much do you feel like listening to acoustic music?") 
        print("( 0 being no acoustic and 10 being acoustic)")

        acousticness = self.attributes[8]

        acousticness *= 0.1

        return {
                "attribute": "acousticness", 
                "match": False,
                "boolv": False,
                "phrase": None, 
                "range": True, 
                "val": acousticness
            }

    # isntrumentalness #####


    def instrumentalness_input(self): 
        print("On a scale of 0 to 10, how much do you want the song to be instrumental?") 
        print("( 0 being not instrumental at all and 10 being only instrumental(no vocals))")

        instrumentalness = self.attributes[9]

        instrumentalness *= 0.1 

        return{
                "attribute": "instrumentalness", 
                "match": False,
                "boolv": False,
                "phrase": None, 
                "range": True, 
                "val": instrumentalness
            }


    # liveness #####

    def liveness_input(self): 

        print("On a scale of 0 to 10, how much do you feel like listening to live music?") 
        print("( 0 being not at all and 10 being a lot)")

        liveness = self.attributes[10]

        liveness *= 0.1 

        return {
                "attribute": "liveness", 
                "match": False,
                "boolv": False,
                "phrase": None, 
                "range": True, 
                "val": liveness
            }

    # tempo #####

    def tempo_input(self): 

        print("On a scale of 0 to 10, how upbeat do you want the song to be?") 
        print("( 0 being no tempo at all and 10 being high tempo)")

        tempo = self.attributes[11]

        tempo *= 0.1 

        return {
                "attribute": "tempo", 
                "match": False,
                "boolv": False,
                "phrase": None, 
                "range": True, 
                "val": tempo
            }
        


    def prompt_user(self): 

        attributeDict = []
        print("PromptUser")
        print(self.attributes)

        attributeDict.append(self.explicit_input())

        print("Is there a specific artist you are searching for?")
        print("0 for no, 1 for yes")

        artist_choice = self.inputs[1]
        if(artist_choice):
            attributeDict.append(self.artist_input())
        

        print("Is there a specific album you are searching for?")
        print("0 for no, 1 for yes")

        album_choice = self.inputs[2]

        if(album_choice):
            attributeDict.append(self.album_input())


        print("Do you want to search by genre?")
        print("0 for no, 1 for yes")

        genre_choice = self.inputs[3]

        if(genre_choice): 
            attributeDict.append(self.genre_input())

        attributeDict.append(self.valence_input())

        attributeDict.append(self.danceability_input())

        attributeDict.append(self.energy_input())
        
        attributeDict.append(self.loudness_input())

        attributeDict.append(self.acousticness_input())
        
        attributeDict.append(self.instrumentalness_input())
        
        attributeDict.append(self.liveness_input())
        
        attributeDict.append(self.tempo_input())

        return attributeDict



    #attributes is the list of mappings that can be used by query_form.py to search es.

    #print(attributes)