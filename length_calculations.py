import spotipy
import requests
import json
import csv
import sqlite3
import matplotlib.pyplot as plt
import os
import numpy as np
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

db = 'Music_Data.db'
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+db)
cur = conn.cursor()

def get_data_from_db():
    #getting the length of each song and writing it to a csv file
    cur.execute('SELECT Length FROM Spotipy')
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
    with open('spotipycalculations.csv', 'w') as fil:
        writer = csv.writer(fil)
        writer.writerow(['Lengths of songs (in minutes)', 'Number of songs'])
        writer.writerow(['< 2:30', shortest])
        writer.writerow(['2:30 - 2:45', two45])
        writer.writerow(['2:45 - 3:00', lessthan3])
        writer.writerow(['3:00 - 3:15', threemin15])
        writer.writerow(['3:15 - 3:30', threemin30])
        writer.writerow(['3:30 - 3:45', threemin45])
        writer.writerow(['3:45 - 4:00', fourmin])
        writer.writerow(['4:00 - 4:15', fourmin15])
        writer.writerow(['> 4:15', fourmin30])

    #getting the length of each song name and writing it to a csv file
    cur.execute('SELECT Song_Name from Spotipy')
    result2 = cur.fetchall()
    one = 0
    two = 0
    three = 0
    four = 0
    morethan4 = 0
    for song in result2:
        if '(' in song[0]:
            song_title = song[0].split('(')
            title_split = song_title[0].split()
        elif '-' in song[0]:
            song_title = song[0].split('-')
            title_split = song_title[0].split()
        else:
            title_split = song[0].split()

        if len(title_split) == 1:
            one += 1
        elif len(title_split) == 2:
            two += 1
        elif len(title_split) == 3:
            three += 1
        elif len(title_split) == 4:
            four += 1
        else:
            morethan4 += 1
    with open('spotipycalculations2.csv', 'w') as fil2:
        writer = csv.writer(fil2)
        writer.writerow(['Lengths of song name (in words)', 'Number of songs', 'Percentage'])
        writer.writerow(['One', one, one/100])
        writer.writerow(['Two', two, two/100])
        writer.writerow(['Three', three, three/100])
        writer.writerow(['Four', four, four/100])
        writer.writerow(['More than four', morethan4, morethan4/100])


def make_lengths_graph():
    x_values = []
    y_values = []
    with open('spotipycalculations.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        for row in csv_reader:
            if count == 0:
                count += 1
                continue
            else:
                x_values.append(row[0])
                y_values.append(float(row[1]))
    plt.bar(x_values, y_values, align='center', color=('red', 'orange', 'yellow', 'green', 'blue', 'purple', 'violet', 'pink', 'maroon'))
    plt.xlabel("Song Length")
    plt.xticks(rotation=90)
    plt.ylabel("Count of Songs per Length")
    plt.title("Number of Songs on Spotify Top 100 by Length")
    plt.savefig("spotify_bargraph.png", bbox_inches='tight')
    plt.tight_layout()
    plt.show()
    return

def make_song_title_graph():
    labels = []
    sizes = []
    with open('spotipycalculations2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        for row in csv_reader:
            if count == 0:
                count += 1
                continue
            else:
                if row[0] == 'One':
                    labels.append(row[0] + ' word')
                else:
                    labels.append(row[0] + ' words')
                sizes.append(row[1])
    plt.pie(sizes, labels = labels, colors = ['teal', 'purple', 'grey', 'lightcoral', 'lightskyblue'], autopct='%1.0f%%')
    plt.axis('equal')
    plt.title("Length of Song Names on Spotify Top 100")
    plt.tight_layout()
    plt.savefig("spotify_piechart.png", bbox_inches='tight')
    plt.show()

    
    return
    

get_data_from_db()
make_lengths_graph()
make_song_title_graph()