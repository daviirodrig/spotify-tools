from urllib.parse import unquote
import base64
import json
import time
from bs4 import BeautifulSoup
import requests


class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_expire = None

    def get_id(self, spotify_input: str):
        # input is uri
        if spotify_input.startswith("spotify:") and len(spotify_input.split(":")) == 3:
            return spotify_input.split(":")[-1]
        # input is url
        else:
            return spotify_input.split("/")[-1].split("?")[0]

    def get_access_token(self):
        if self.access_token:
            now = int(time.time())
            if now < self.access_token_expire:
                return self.access_token
        auth_to_encode = f"{self.client_id}:{self.client_secret}".encode(
            "ascii")
        auth_b64 = base64.b64encode(auth_to_encode)
        body = {"grant_type": "client_credentials"}
        header = {"Authorization": f"Basic {auth_b64.decode('ascii')}"}
        res = requests.post(
            "https://accounts.spotify.com/api/token", data=body, headers=header)
        access_token = res.json().get("access_token")
        self.access_token = access_token
        self.access_token_expire = int(time.time()) + 3600
        return access_token

    def get_song_json(self, song):
        song_id = self.get_id(song)
        access_token = self.get_access_token()
        header = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/tracks/{song_id}"
        res_json = requests.get(base_url, headers=header).json()

        # Get preview_url with scraping when spotify api does not return it
        if res_json["preview_url"] is None:
            req = requests.get(
                f"https://open.spotify.com/embed/track/{res_json['id']}").text
            soup = BeautifulSoup(req, "html.parser")
            script_json = unquote(soup.find("script", id="resource").string)
            song_json = json.loads(script_json)
            res_json["preview_url"] = song_json["preview_url"]

        return res_json

    def get_playlist_json(self, playlist):
        playlist_id = self.get_id(playlist)
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        res_json = requests.get(base_url, headers=headers).json()
        return res_json
