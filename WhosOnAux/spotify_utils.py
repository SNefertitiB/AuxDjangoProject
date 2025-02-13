from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from typing import List

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_token() -> str:
    # create authorization string to be encoded with base64
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers ,data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token:str) -> dict:
    return {"Authorization": "Bearer " + token}

class SpotifyPlaylist:
    def __init__(self, playlist_id:str) -> None:
        self.playlist_id = playlist_id
        self.token = get_token()
        # GET /playlists/{playlist_id}
        self.headers = get_auth_header(self.token)


    def get_tracks(self) -> dict:
        """
        use item['track']['name'] to get names
        use item['track']['id'] to get id
        use
        :return: items:dict
        """
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        result = get(url, headers=self.headers)
        json_result = json.loads(result.content)['items']
        tracks = []
        return json_result

    def get_image_details(self) -> List[dict]:
        """
        json_result[index]['url']
        json_result[index]['height'] in pixels
        json_result[index]['width'] in pixels
        :return: json_result: list of dict
        """
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/images"
        result = get(url, headers=self.headers)
        json_result = json.loads(result.content)
        return json_result