import os
import base64
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
SP_CLIENT_SECRET = os.environ.get("SP_CLIENT_SECRET")
SP_CLIENT_ID = os.environ.get("SP_CLIENT_ID")


def get_access_token():
    auth_to_encode = f"{SP_CLIENT_ID}:{SP_CLIENT_SECRET}".encode("ascii")
    auth_b64 = base64.b64encode(auth_to_encode)
    body = {"grant_type": "client_credentials"}
    header = {"Authorization": f"Basic {auth_b64.decode('ascii')}"}
    res = requests.post(
        "https://accounts.spotify.com/api/token", data=body, headers=header)
    access_token = res.json().get("access_token")
    return access_token


def get_song_json(song_uri):
    song_uri = song_uri.split(":")[-1]
    access_token = get_access_token()
    header = {"Authorization": f"Bearer {access_token}"}
    base_url = f"https://api.spotify.com/v1/tracks/{song_uri}"
    res_json = requests.get(base_url, headers=header).json()
    return res_json


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/details")
def details():
    song_uri = request.args.get("songURI")
    if song_uri in (None, ""):
        return render_template("detailsForm.html")
    song_json = get_song_json(song_uri)
    return render_template("details.html", song_json=song_json)
