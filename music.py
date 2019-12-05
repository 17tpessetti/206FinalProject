# here are examples for api calls for musixmatch
import requests
import json
import sqlite3
import os

musixmatch_api = '12d054c3145863550c882f72f39fdb15'
baseurl = "https://api.musixmatch.com/ws/1.1/"
format_url = "?format=json&callback=callback"

api_call_italy = 'https://api.musixmatch.com/ws/1.1/chart.tracks.get?chart_name=top&page=1&page_size=5&country=it&f_has_lyrics=1&apikey=12d054c3145863550c882f72f39fdb15'
api_call_us = 'https://api.musixmatch.com/ws/1.1/chart.tracks.get?chart_name=top&page=1&page_size=100&country=us&f_has_lyrics=1&apikey=12d054c3145863550c882f72f39fdb15'
request = requests.get(api_call_us)
data = request.json()
print(api_call_us)