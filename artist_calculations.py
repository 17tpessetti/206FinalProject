import requests
import json
import csv
import sqlite3
import matplotlib_venn as vplt
from matplotlib import pyplot as plt

import os

db = 'Music_Data.db'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db)
cur = conn.cursor()


def get_favs_from_db():
    cur.execute('SELECT Num_Favorite FROM Hot_100_Musixmatch_Artists WHERE Artist ="Billie Eilish"')
    total = 0
    result = cur.fetchall()
    for item in result:
        total += item[0]
    with open('musixmatchcalculations.csv','w') as fil:
        w = csv.writer(fil)
        w.writerow(['Artist','Total Number of Favorties'])
        w.writerow(["Billie Eilish",total])



def get_common_song_id():
    sql = "SELECT * \
    FROM Spotipy_Ids\
    LEFT JOIN Hot_100_Musixmatch_Songs\
    ON Spotipy_Ids.Song_Name = Hot_100_Musixmatch_Songs.Song_Name"
    cur.execute(sql)
    cur.execute("SELECT COUNT(Musixmatch_id) FROM Spotipy_Ids")
    result = cur.fetchone()
    spotify = 100-result
    musixmatch = 100-result
    musixmatch_per = 100-result/100
    shared = result
    total_shared = result/100
    with open('dbcalculation.csv', 'w') as fil:
        w = csv.writer(fil)
        w.writerow(['Songs only on Spotify','Songs only on Musixmatch','Shared Songs','percentage'])
        w.writerow([spotify,musixmatch,shared,total_shared])


def make_shared_chart():
    v = vplt.venn2(subsets={'10': 100, '01': 100, '11': 36}, set_labels = ('A', 'B'),set_colors=('g','b'))
    v.get_label_by_id('A').set_text('Spotify')
    v.get_label_by_id('B').set_text('MusixMatch')
    plt.show()


get_favs_from_db() #total number of favorites for artist Billie Eilish
get_common_song_id()
make_shared_chart()