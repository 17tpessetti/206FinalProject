import spotipy
import requests
import json
import sqlite3
import os
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data


db = 'Spotipy_Data.db'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db)
cur = conn.cursor()

#setting up the API
token = util.prompt_for_user_token(username = '17tpessetti', scope = 'user-top-read', client_id = '5933ae69691d4b44b764d94b1b0c1fac', client_secret = '633d85761ffd4a3ab7bacab55a8a9bdd', redirect_uri = 'https://example.com/callback/')
spotify = spotipy.Spotify(auth = token)
user = spotify.current_user()
displayName = user['display_name']

#creating the database
def create_database():
    cur.execute('CREATE TABLE IF NOT EXISTS Top_100_Spotipy(Song_Name TEXT, Artist TEXT, Length FLOAT)')

#getting the playlist
def get_playlist(username, playlist_name):
    playlists = spotify.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            final_playlist = playlist
            return final_playlist['id']


def get_tracks(playlist):
    user_id = '17tpessetti'
    playlist = get_playlist(user_id, playlist)
    tracks = spotify.user_playlist_tracks(user_id, playlist, limit = 100)
    songs_list = []
    count = 0
    for song in tracks['items']:
        song_name = song['track']['name']
        artist = song['track']['artists'][0]['name']
        length = song['track']['duration_ms']/1000
        cur.execute("SELECT song_name FROM Top_100_Spotipy WHERE song_name=?", (song_name, ))
        result = cur.fetchone()
        if result:
            continue
        else:
            cur.execute("INSERT INTO Top_100_Spotipy (Song_Name, Artist, Length) VALUES (?,?,?)", (song_name, artist, length))
            count += 1
            conn.commit()
        if count == 20:
            break           

create_database()
get_tracks('US Top 100 SI 206')

