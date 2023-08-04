from flask import Flask, request
import sys
sys.path.append( '../')
from es_testing import execElasticSearch
app = Flask(__name__)

@app.route("/members")
def members():
    return {"members": ["Member1","Member3","Member3"]}

@app.route("/prompt")
def prompt():

    return {"prompts": [
        "On a scale of 0 to 10, how do you want to feel after hearing this song? \n(0 being sad/bad and 10 being happy/good)",
        "On a scale of 0 to 10, how much do you feel like dancing? \n ( 0 being not at all and 10 being I WANNA DANCE)",
        "On a scale of 0 to 10, how much energy do you want from a song rn? \n ( 0 being not nuch energy and 10 being all the enegry there is)",
        "How loud do you want the song to be? \n ( 0 being quiet and 10 being loud) ",
        "On a scale of 0 to 10, how much do you feel like listening to acoustic music? \n ( 0 being no acoustic and 10 being acoustic)",
        "On a scale of 0 to 10, how much do you want the song to be instrumental? \n ( 0 being not instrumental at all and 10 being only instrumental(no vocals))",
        "On a scale of 0 to 10, how much do you feel like listening to live music? \n ( 0 being not at all and 10 being a lot)",
        "On a scale of 0 to 10, how upbeat do you want the song to be? \n ( 0 being no tempo at all and 10 being high tempo)",

        ]}

@app.route('/answers', methods=['POST'])
def prompt_input():
    
    #print(request.json, file=sys.stderr)
    songs = execElasticSearch(request.json)
    print(songs) 
    
    return {"songList": songs}

if __name__  == "__main__":
    app.run(debug=True)