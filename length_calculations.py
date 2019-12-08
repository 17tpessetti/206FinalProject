import spotipy
import requests
import json
import sqlite3
import os
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

db = 'Music_Data.db'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db)
cur = conn.cursor()

def get_lengths_from_db():
    cur.execute('SELECT length FROM Spotipy')
    result = cur.fetchall()
    shortest = 0
    two45 = 0
    lessthan3 = 0
    threemin15 = 0
    threemin30 = 0
    threemin45 = 0
    fourmin = 0
    fourmin15 = 0
    fourmin30 = 0
    lengths = []
    for item in result:
        item_seconds = round(item[0]) #rounds to the nearest second
        lengths.append(item_seconds)
        if item_seconds < 150:
            shortest += 1
        elif item_seconds < 165:
            two45 += 1
        elif item_seconds < 180:
            lessthan3 += 1
        elif item_seconds < 195:
            threemin15 += 1
        elif item_seconds < 210:
            threemin30 += 1
        elif item_seconds < 225:
            threemin45 += 1
        elif item_seconds < 240:
            fourmin += 1
        elif item_seconds < 255:
            fourmin15 += 1
        else:
            fourmin30 += 1
    print(shortest, two45, lessthan3, threemin15, threemin30, threemin45, fourmin, fourmin15, fourmin30)
get_lengths_from_db()