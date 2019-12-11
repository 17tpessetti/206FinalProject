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
    result = cur.fetchall()
    shared_counter = 0
    for x in result:
        if x[3] != None:
            shared_counter+=1
    spotify = 100-shared_counter
    musixmatch = 100-shared_counter
    shared = shared_counter
    total_shared = shared_counter/100
    with open('dbcalculation.csv', 'w') as fil:
        w = csv.writer(fil)
        w.writerow(['Songs only on Spotify','Songs only on Musixmatch','Shared Songs','percentage'])
        w.writerow([spotify,musixmatch,shared,total_shared])


def make_shared_chart():
    spot_only = 0
    musix_only = 0
    shared = 0
    with open ('dbcalculation.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        for row in csv_reader:
            if count == 0:
                count += 1
                continue
            else:
                spot_only = float(row[0])
                musix_only = float(row[1])
                shared = float(row[2])
    v = vplt.venn2(subsets={'10': spot_only, '01': musix_only, '11': shared}, set_labels = ('A', 'B'),set_colors=('g','b'))
    v.get_label_by_id('A').set_text('Spotify')
    v.get_label_by_id('B').set_text('MusixMatch')
    plt.title("Shared Songs Between Spotify and Musixmatch")
    plt.show()


get_favs_from_db() #total number of favorites for artist Billie Eilish
get_common_song_id()
make_shared_chart()