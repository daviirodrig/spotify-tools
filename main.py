import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request
from spotify_utils import Spotify

load_dotenv(".env")
app = Flask(__name__)
SP_CLIENT_SECRET = os.environ.get("SP_CLIENT_SECRET")
SP_CLIENT_ID = os.environ.get("SP_CLIENT_ID")
sp = Spotify(SP_CLIENT_ID, SP_CLIENT_SECRET)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/details")
def details():
    song_uri = request.args.get("songURI")
    if song_uri in (None, ""):
        return render_template("detailsForm.html")
    song_json = sp.get_song_json(song_uri)
    delta = str(timedelta(milliseconds=song_json["duration_ms"])).split(":")
    duration = f"{delta[1]}:{delta[2].split('.')[0]}"
    song_json["duration"] = duration
    artists = [i["name"] for i in song_json["artists"]]
    artists_str = ', '.join(artists)
    song_json["artists_str"] = artists_str
    return render_template("details.html", song_json=song_json)


@app.route("/playlistvis")
def playlistviz():
    playlist_uri = request.args.get("playlistURI")
    if playlist_uri in (None, ""):
        return render_template("playlistForm.html")
    playlist_json = sp.get_playlist_json(playlist_uri)
    return render_template("playlist.html", playlist_json=playlist_json)
