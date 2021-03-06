import base64
import requests


class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_access_token(self):
        auth_to_encode = f"{self.client_id}:{self.client_secret}".encode(
            "ascii")
        auth_b64 = base64.b64encode(auth_to_encode)
        body = {"grant_type": "client_credentials"}
        header = {"Authorization": f"Basic {auth_b64.decode('ascii')}"}
        res = requests.post(
            "https://accounts.spotify.com/api/token", data=body, headers=header)
        access_token = res.json().get("access_token")
        return access_token

    def get_song_json(self, song_uri):
        song_uri = song_uri.split(":")[-1]
        access_token = self.get_access_token()
        header = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/tracks/{song_uri}"
        res_json = requests.get(base_url, headers=header).json()
        return res_json

    def get_playlist_json(self, playlist_uri):
        playlist_id = playlist_uri.split(":")[-1]
        access_token = self.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        base_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        res_json = requests.get(base_url, headers=headers).json()
        return res_json
