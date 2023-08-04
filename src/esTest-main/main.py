
from flask import Flask, request, jsonify

from prompt_manager import PromptManager
from es_execute import  execute
from spotify import Spotify
from flask_cors import CORS
from es_manager import ESManager

app = Flask(__name__)
CORS(app)


es_instance = ESManager()
es_instance.set_up_index()
promptManager = PromptManager()

@app.route("/execute_es", methods=["POST"])
def execute_es():
    
    
    promptManager.build_new()
    

    resp = {"prompt": "es started"}

    return jsonify(resp)


@app.route("/get_prompt", methods=["POST"])
def get_prompt():


    request_obj = request.get_json(force=True)
    
    promptManager.response = request_obj
    prompt = promptManager.prompt_user()
   
    print("-------------------")
    print(promptManager.attributes)
    

    jsonData = {"prompt": prompt}
    print(jsonData)

    return jsonify(jsonData)

@app.route("/fetch_recommendations", methods=["GET"])
def receive_input():


    songList = execute(prompt_man=promptManager, es_man=es_instance)
    print('___________________fetch_______________________')

    spotify = Spotify(songList)
    print(songList)
    songs = spotify.search_ids()
    return jsonify(songs)


if __name__  == "__main__":
    app.run(debug=True, port=3001)
    
     