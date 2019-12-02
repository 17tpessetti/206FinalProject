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

#creating the database
def create_database():
    cur.execute('CREATE TABLE IF NOT EXISTS Top_20_Spotipy(Song_Name TEXT, Artist TEXT, Length FLOAT, Country TEXT)')

def read_data(fil):
    full_path = os.path.join(os.path.dirname(__file__), fil)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def insert_values(data_file):
    data = read_data(data_file)
    for country in data:
        for song in data[country]:
            cur.execute("INSERT INTO Top_20_Spotipy (Song_Name, Artist, Length, Country) VALUES (?,?,?,?)", (song['song_name'], song['artist'], song['length'], country))
    conn.commit()


#checks to see if data was already input into the database, and if it wasn't, then it inputs the data - if it was, it does not duplicate the data
create_database()
song = cur.execute('SELECT Song_Name from Top_20_Spotipy WHERE Artist = ?', ('Lunay', ))
s = cur.fetchone()
if (type(s) != tuple):
    insert_values('data.txt')