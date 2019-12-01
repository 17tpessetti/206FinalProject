import spotipy
import requests
import json
import sqlite3
import os
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data


# client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
token = util.prompt_for_user_token(username = '17tpessetti', scope = 'user-top-read', client_id = '5933ae69691d4b44b764d94b1b0c1fac', client_secret = '633d85761ffd4a3ab7bacab55a8a9bdd', redirect_uri = 'https://example.com/callback/')
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API
spotify = spotipy.Spotify(auth = token)
user = spotify.current_user()
displayName = user['display_name']


def get_playlist(username, playlist_name):
    playlists = spotify.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            final_playlist = playlist
            return final_playlist['id']

def get_top_20_tracks(playlist, country):
    user_id = '17tpessetti'
    playlist = get_playlist(user_id, playlist)
    tracks = spotify.user_playlist_tracks(user_id, playlist, limit = 20)
    songs_list = []
    for song in tracks['items']:
        d = {}
        d['song_name'] = song['track']['name']
        d['artist'] = song['track']['artists'][0]['name']
        d['length'] = song['track']['duration_ms']/1000
        songs_list.append(d)
    return songs_list

aus = get_top_20_tracks('Australia Top 50 SI 206', 'Australia')

large_dict = {}
large_dict['Australia'] = aus

with open('data.txt', 'w') as json_file:
    json.dump(large_dict, json_file)


def create_atabase(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Top_20(Song_Name TEXT, Artist TEXT, Length FLOAT, country TEXT)')




#here are examples for api calls for musixmatch


musixmatch_api = '12d054c3145863550c882f72f39fdb15'
baseurl = "https://api.musixmatch.com/ws/1.1/"
format_url = "?format=json&callback=callback"

api_call_italy = 'https://api.musixmatch.com/ws/1.1/chart.tracks.get?chart_name=top&page=1&page_size=5&country=it&f_has_lyrics=1&apikey=12d054c3145863550c882f72f39fdb15'
api_call_us = 'https://api.musixmatch.com/ws/1.1/chart.tracks.get?chart_name=top&page=1&page_size=5&country=us&f_has_lyrics=1&apikey=12d054c3145863550c882f72f39fdb15'
request = requests.get(api_call_us)
data = request.json()
print(api_call_us)