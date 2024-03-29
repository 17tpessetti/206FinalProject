# here are examples for api calls for musixmatch
import requests
import json
import sqlite3
import os


db = 'Music_Data.db'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db)
cur = conn.cursor()


musixmatch_api = '12d054c3145863550c882f72f39fdb15'
baseurl = "https://api.musixmatch.com/ws/1.1/"
format_url = "?format=json&callback=callback"



def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS Hot_100_Musixmatch_Artists(Song_Name TEXT, Artist TEXT, Num_Favorite INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Hot_100_Musixmatch_Songs(Song_Name TEXT, Musixmatch_id INTEGER)")


api_call_us = 'https://api.musixmatch.com/ws/1.1/chart.tracks.get?chart_name=mxmweekly&page_size=100&country=us&apikey=12d054c3145863550c882f72f39fdb15'

def get_tracks(api):
    request = requests.get(api)
    top_100_us = request.json()
    count = 0
    for song in top_100_us["message"]["body"]["track_list"]:
        song_name = song["track"]["track_name"]
        artist = song["track"]["artist_name"]
        song_id = song["track"]["track_id"]
        num_favorite = song["track"]["num_favourite"]
        cur.execute("SELECT song_name FROM Hot_100_Musixmatch_Artists WHERE song_name=?", (song_name, ))
        result = cur.fetchone()
        if result:
            continue
        else:
            cur.execute("INSERT INTO Hot_100_Musixmatch_Artists (Song_Name, Artist, Num_Favorite) VALUES (?,?,?)", (song_name,artist,num_favorite))
            cur.execute("INSERT INTO Hot_100_Musixmatch_Songs (Song_Name, Musixmatch_id) VALUES (?,?)", (song_name, song_id))
            count += 1
            conn.commit()
        if count == 20:
            break



create_table()
get_tracks(api_call_us)
print(api_call_us)