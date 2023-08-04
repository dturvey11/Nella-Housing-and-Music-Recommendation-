import base64
import requests
import json

class Spotify():

    def __init__(self, ids):
        self.ids = ids

        self.access_token = self.authenticate()


    def authenticate(self):
        CLIENT_ID = '28a64b7e033b4433baf6eccbe79b7a67';
        CLIENT_SECRET = 'bc4be37184204626a2b31fbdd0326e66';
    
        client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
        client_creds_base64 = base64.b64encode(client_creds.encode())

        tokenURL = 'https://accounts.spotify.com/api/token'

        METHOD = "POST"

        token_data = {
            "grant_type" : "client_credentials"
        }

        token_headers = {
            "Authorization" : f"Basic {client_creds_base64.decode()}"
        }

        req = requests.post(tokenURL, data=token_data, headers=token_headers)
        token_response_data = req.json()

        access_token = token_response_data['access_token']

        return access_token
    
    def search_ids(self):

        parsed_song_info = []
        print("-----------------")
        print(self.ids)
        for id in self.ids:
            req = self.__search_id(id);
            parsed_song_info.append(    #req["tracks"][0] will always be 0 because a search onnly returns one songg
                {
                    "name": req["tracks"][0]["name"],
                    "artist": req["tracks"][0]["artists"][0]["name"],
                    "url": req["tracks"][0]["external_urls"]["spotify"],
                    "cover_url": req["tracks"][0]["album"]["images"][0]["url"],
                    "album": req["tracks"][0]["album"]["name"],
                    "track_id": id,
                }
            )
        return (parsed_song_info)

    def __search_id(self, id):

        end_point = 'https://api.spotify.com/v1/tracks?ids='


        header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        lookup_url = end_point + id
        req = requests.get(lookup_url, headers=header)

        return req.json()





