import requests
import json
import csv
import sqlite3
import matplotlib.pyplot as plt
import os
import numpy as np

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

get_favs_from_db() #total number of favorites for artist Billie Eilish